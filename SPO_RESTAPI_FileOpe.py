import json
import requests
import os
import sys

# SSL警告対策(warning無効化)
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

input_url= sys.argv[1]


# 下記は変更不要（TMCのテナントID、固定）
t_postfix='@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8'

# 下記を都度変更（クライアントID、クライアントシークレット）
c_id=*****
c_secret=*****

# SharePointサイトのURLを設定
base_url = "https://toyotajp.sharepoint.com/sites/msteams_c8478b-91_Artifacts_private/"

#############################################################################################################################################
# トークン取得
url = 'https://accounts.accesscontrol.windows.net/d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8/tokens/OAuth/2'
data = {
    'grant_type':'client_credentials',
    'client_id': c_id,
    'client_secret': c_secret,
    'resource':'00000003-0000-0ff1-ce00-000000000000/toyotajp.sharepoint.com@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8',
}
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
}
r = requests.post(url, data=data, headers=headers)
json_token = json.loads(r.text)


#############################################################################################################################################
# ファイルアップロード用のFormDigestValue値を取得
# query url
url = "https://toyotajp.sharepoint.com/sites/msteams_c8478b-91_Artifacts_private/_api/contextinfo"
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
    'Accept':'application/json;odata=verbose',
}
r = requests.post(url, headers=headers)
json_response =  json.loads(r.text)
digest_value = json_response['d']['GetContextWebInformation']['FormDigestValue']

# debug print (json_response)
# debug print (digest_value)



#############################################################################################################################################
# フォルダ作成
# https://qiita.com/zenpou/items/eb3b0bb61c06bb932723
# query url
url = base_url + '_api/web/folders'

## フォルダ名指定
#下記は固定前提 (Shared Documents配下にフォルダを作成する前提)
PARENT = 'Shared%20Documents/'
# 下記は変動させても良い
folder_name = 'test123'
t_folder_url = '/sites/msteams_c8478b-91_Artifacts_private/' + PARENT + folder_name

# 送信データ作成
data={
    '__metadata': {
        'type': 'SP.Folder'
    },
  'ServerRelativeUrl': t_folder_url  
}

#AcceptとContent-Typeに注意(odata必要)
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Type': "application/json;odata=verbose",
    'Content-Length': str(len(data)),
    'X-RequestDigest': digest_value
}

###実行部###
#json.dumpsで変換を入れると良い(dataのみだと動きがイマイチ)
l = requests.post(url, data=json.dumps(data), headers=headers)
response =  json.loads(l.text)


#ERROR時のデバッグ用
# print ("ERROR:")
# error_code = response['error']['code'] 
# error_msg = response['error']['message']
# print(error_code)
# print(error_msg)

#############################################################################################################################################
# ファイル作成作成

#下記は固定前提 (Shared Documents配下のフォルダにファイルを作成する前提)
PARENT = 'Shared%20Documents/'
# 下記は変動させても良い
folder_name = '91_Artifacts_private'

# アップロードしたときのファイル名（変動か
upload_fname= 'dummy.txt'

# 上書き設定
overwrite_setting = 'overwrite=true'

# query url
url = base_url  + "_api/web/GetFolderByServerRelativeUrl('" + PARENT + folder_name + "')/Files/add(url='" + upload_fname + "'," + overwrite_setting + ")"


#t_fullpath = os.path.join(os.getcwd(), upload_fname)
t_fullpath = r"C:\Users\1485001\Desktop\back\dummy.txt"

# データ取得(fopen)
with open( t_fullpath, 'rb') as f:
    data2 = f.read()

# ヘッダ生成
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Length': str(len(data2)),
    'X-RequestDigest': digest_value
}

###実行部### # dataは生で
#l = requests.post(url, data=data2, headers=headers)
#response =  json.loads(l.text)

#ERROR時のデバッグ用
# print ("ERROR:")
# error_code = response['error']['code'] 
# error_msg = response['error']['message']
# print(error_code)
# print(error_msg)


# extract filename from input_url
#input_url="https://toyotajp.sharepoint.com/sites/msteams_c8478b-91_Artifacts_private/Shared%20Documents/91_Artifacts_private/20210928_005913_master_4123_lnkm_6310e67.zip"
split_path = os.path.split(input_url)
dl_fname=split_path[1]

#############################################################################################################################################
# ファイルダウンロード
url = base_url + "_api/web/GetFolderByServerRelativeUrl('" + PARENT + folder_name + "')/Files('" + dl_fname + "')/$value"
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
}
response = requests.get(url, headers=headers)
#print(response.text)
    
#HTTP Responseのエラーチェック
try:
    response_status = response.raise_for_status()
except Exception as exc:
    print("Error:{}".format(exc))


#t_fullpath = os.path.join(os.getcwd(), dl_fname)
t_fullpath = "C:/Users/1485001/Desktop/back/" + dl_fname
print (t_fullpath)
print ("Now downloading...")

# HTTP Responseが正常な場合は下記実行
if response_status == None:
    #open()関数にwbを渡し、バイナリ書き込みモードで新規ファイル生成
    file = open(t_fullpath,"wb")

    #各チャンクをwrite()関数でローカルファイルに書き込む
    #100000 = 100KBらしい
    for chunk in response.iter_content(100000):
        file.write(chunk)

    #ファイルを閉じる
    file.close()
#############################################################################################################################################



exit(0)
