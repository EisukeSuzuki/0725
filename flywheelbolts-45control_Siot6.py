import sys
from time import sleep
from serial.tools import list_ports  # ポートリスト取得用
from pykeigan import usbcontroller
from pykeigan import utils
import SiOt_module  # SiOtモジュール用のライブラリ

def find_keigan_motor():
    """
    Keiganモーターが接続されているポートを自動的に検出する。
    """
    ports = list_ports.comports()
    for port in ports:
        if "Keigan" in port.description or "ttyUSB" in port.device:  # Keiganモーターの識別条件
            return port.device
    return None
    
def initialize_motor(dev):
    """
    Keiganモーターの初期化を行い、トルクをかける。
    """
    print("モーターを有効化してトルクをかけます。")
    dev.enable_action()
    sleep(1)
    
    print("0度回転させてフリー状態を解除します。")
    dev.move_by_dist(utils.deg2rad(0))  # 0度回転
    sleep(2)  # 回転完了まで待機

    print("トルクが有効になりました。")    


def rotate_motor_45_degrees_8_times(dev, SIO):
    """
    SiOtモジュールの信号に基づいてモーターを45度ずつ8回回転させる。
    回転後、完了信号をSiOtモジュールに出力する。
    """
    print("モーターを45度ずつ8回回転させます (ワーク有り条件付き)。")
    dev.enable_action()
    dev.set_speed(utils.rpm2rad_per_sec(10))  # 回転速度設定 (rpm -> rad/sec)

    for i in range(8):
        print(f"{i + 1}回目の回転を開始します。ワーク有りを待機中...")
        while SIO.input_i(3) != 1:  # ワーク有りになるまで待機
            sleep(1)

        print(f"ワーク有りを検出しました。モーターを45度回転します。")
        dev.move_by_dist(utils.deg2rad(-45))  # 45度回転
        sleep(2)  # 回転後少し待機

    print("45度ずつ8回転が完了しました。")
    sleep(1)
    
    # ストッパー閉じ信号を1秒間出力
    print("ストッパー閉じ信号を出力します")
    SIO.ether(4, SIO.ON)  # OUTピン4をON
    sleep(1)
    SIO.ether(4, SIO.OFF)  # OUTピン4をOFF
    print("ストッパー閉じ信号の出力が終了しました。")
    
    # 位置をリセット
    print("累積誤差防止のため、現在位置をリセットします。")
    dev.preset_position(0)
    
    print("22.5度回転まで1秒待機します。")
    sleep(1)
    dev.move_by_dist(utils.deg2rad(22.5))  # 22.5度回転
    sleep(1)

    # 完了信号を1秒間出力
    print("完了信号を出力します。")
    SIO.ether(1, SIO.ON)  # OUTピン1をON
    sleep(1)
    SIO.ether(1, SIO.OFF)  # OUTピン1をOFF
    print("完了信号の出力が終了しました。")

def main_loop():
    """
    モーター動作とワーク検出を無限ループで繰り返す。
    初期化は最初だけ行い、接続を維持。
    """
    # 最初にSiOtモジュールの初期化とモーター接続を行う
    motor_port = find_keigan_motor()
    if not motor_port:
        print("Keiganモーターが検出されませんでした。接続を確認してください。")
        return

    print(f"Keiganモーターが検出されました: {motor_port}")

    # SiOtモジュールの初期化
    SIO = SiOt_module.translator("100.100.1.100", 40001)  # SiOtモジュールのIPアドレスとポート
    print("SiOtモジュールに接続しました。")

    # モーターに接続
    dev = usbcontroller.USBController(motor_port, False)
    
    # モーターの初期化
    initialize_motor(dev)
    
    #起動可信号を出力
    print("起動できます。起動可信号を出力します。")
    SIO.ether(2, SIO.ON)
    sleep(1)
    SIO.ether(2, SIO.OFF)
    print("起動可信号の出力が完了しました。")
                    
    try:
        while True:
            try:
                # 起動スイッチを待機
                print("起動スイッチを待機中...")
                while SIO.input_o(16) != 1:  # 起動スイッチがONになるまで待機
                    sleep(0.1)
                    
                dev.enable_action()  # トルクをON
                dev.set_speed(utils.rpm2rad_per_sec(10))  # 回転速度設定 (rpm -> rad/sec)
                sleep(1)    

                print("起動スイッチが押されました。サイクルを開始します。")
                dev.move_by_dist(utils.deg2rad(-22.5))  # 22.5度回転
                sleep(1)
                
                print("サイクルを開始します。")#45度ずつ8回回転
                rotate_motor_45_degrees_8_times(dev, SIO)

                # 次のサイクルを待機
                print("次のサイクルを待機中です...\n")
                sleep(5)

            except Exception as e:
                print(f"エラーが発生しました: {e}")
                print("5秒後に再試行します...")
                sleep(5)

    except KeyboardInterrupt:
        print("プログラムが中断されました。モーターを停止します。")
        dev.disable_action()
        dev.set_led(1, 0, 0, 0)  # LED消灯

    finally:
        print("プログラムが終了しましたが、モーター接続は維持します。必要に応じて手動で切断してください。")

if __name__ == "__main__":
    main_loop()

