import json
import requests

#####################################################################
### 基本情報 ###
target_SiteName = '<ここに対象のSPOサイト名を入力>'
client_id = '<ここにクライアントIDを入力>@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8'
client_secret = '<ここにクライアントシークレットを入力>'
target_ListName = '<ここにリスト名を入力>'
#####################################################################


#####################################################################
### アクセストークン取得 ###
url = 'https://accounts.accesscontrol.windows.net/d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8/tokens/OAuth/2'
data = {
    'grant_type':'client_credentials',
    'client_id':client_id,
    'client_secret':client_secret,
    'resource':'00000003-0000-0ff1-ce00-000000000000/toyotajp.sharepoint.com@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8',
}
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
}

t = requests.post(url, data=data, headers=headers)
json_token = json.loads(t.text)
#####################################################################


#####################################################################
### リスト操作 ###
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
    'Accept':'application/json;odata=verbose',
}

url = "https://toyotajp.sharepoint.com/sites/"+ target_SiteName +"/_api/web/lists/GetByTitle('"+ target_ListName +"')/items"
# url = "https://toyotajp.sharepoint.com/sites/"+ target_SiteName +"/_api/web/lists/GetByTitle('"+ target_ListName +"')?$select=ListItemEntityTypeFullName"
l = requests.get(url, headers=headers)
print('---------ココから中身---------')
print(l.text)
#####################################################################
