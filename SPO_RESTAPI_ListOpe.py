import json
import requests

#####################################################################
### 基本情報 ###
target_SiteName = '<ここに対象のSPOサイト名を入力>'
client_id = '<ここにクライアントIDを入力>@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8'
client_secret = '<ここにクライアントシークレットを入力>'
target_ListName = '<ここにリスト名を入力>'
target_ListEntityName = '<ここに内部リスト名を入力>'
target_ListItemID = '<ここにリストアイテムIDを入力>'
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

r = requests.post(url, data=data, headers=headers)
json_token = json.loads(r.text)
#####################################################################


#####################################################################
### リストアイテム作成 ###
url = "https://toyotajp.sharepoint.com/sites/"+ target_SiteName +"/_api/web/lists/GetByTitle('"+ target_ListName +"')/items"
data = '''{
    "__metadata": {
        "type": "'''+ target_ListEntityName +'''"
    },
    "Title": "Title by python"
}'''
headers = {
    'Authorization': 'Bearer ' + json_token['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose',
    'Content-Length': str(len(data)),
}

l = requests.post(url, data=data, headers=headers)
print('---------リストアイテム作成---------')
print(l.text)
#####################################################################


#####################################################################
### リストアイテム更新 ###
# url = "https://toyotajp.sharepoint.com/sites/"+ target_SiteName +"/_api/web/lists/GetByTitle('"+ target_ListName +"')/items("+ target_ListItemID +")"
# data = '''{
#     "__metadata": {
#         "type": "'''+ target_ListEntityName +'''"
#     },
#     "Title": "Title update by python"
# }'''
# headers = {
#     'Authorization': 'Bearer ' + json_token['access_token'],
#     'Accept':'application/json;odata=verbose',
#     'Content-Type': 'application/json;odata=verbose',
#     'Content-Length': str(len(data)),
#     'If-Match': '*',
#     'X-HTTP-Method': 'MERGE'
# }

# l = requests.post(url, data=data, headers=headers)
# print('---------リストアイテム更新---------')
# print(l.text)
#####################################################################


#####################################################################
### リストアイテム削除 ###
# url = "https://toyotajp.sharepoint.com/sites/"+ target_SiteName +"/_api/web/lists/GetByTitle('"+ target_ListName +"')/items("+ target_ListItemID +")"
# headers = {
#     'Authorization': 'Bearer ' + json_token['access_token'],
#     'Accept':'application/json;odata=verbose',
#     'Content-Type': 'application/json',
#     'If-Match': '*',
#     'X-HTTP-Method': 'DELETE'
# }

# l = requests.post(url, headers=headers)
# print('---------リストアイテム削除---------')
# print(l.text)
#####################################################################
