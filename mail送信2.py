import smtplib
from email.mime.text import MIMEText

smtp_server = "smtp.office365.com"
port = 587
sender_email = "eisuke_suzuki_aa@mail.toyota.co.jp"
receiver_email = "eisuke_suzuki_aa@mail.toyota.co.jp"
password = "j*158588"

message = MIMEText('これはテストメールです。')
message['Subject'] = 'テスト'
message['From'] = sender_email
message['To'] = receiver_email

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print('メールが送信されました')
except Exception as e:
    print(f'エラーが発生しました: {e}')
finally:
    server.quit()
