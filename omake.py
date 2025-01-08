# おまけ情報用/所々削除したためつじつまが合わない可能性あり #
from typing import Any
from numpy import arange
import openpyxl
import csv
import pandas
import datetime
import shutil
import json
import requests
import codecs
import os
import sys


#CSV to JSON################################################
keys = (    
    "OData__x66f8__x985e_ID",
    "Title",
    "OData__x66f8__x985e__x30d0__x30fc__x30",
    "OData__x6dfb__x4ed8__x6709__x7121_",
    "OData__x30b3__x30e1__x30f3__x30c8__x67",
    "OData__x95a2__x9023__x66f8__x985e__x67",
    "OData__x30d5__x30a9__x30fc__x30e0__x30",
    "OData__x30d5__x30a9__x30fc__x30e0__x54",
    "OData__x30d5__x30a9__x30fc__x30e0__x300",
    "OData__x56de__x4ed8__x30eb__x30fc__x30",
    "OData__x56de__x4ed8__x30eb__x30fc__x300",
    "OData__x56de__x4ed8__x30eb__x30fc__x301",
    "OData__x66f8__x985e__x72b6__x614b_",
    "OData__x73fe__x5728__x306e__x30b9__x30",
    "OData__x57fa__x6e96__x65e5_"
)
json_list = []

# 対象ファイル名生成 #
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
yesterday_format = "{0:%Y%m%d}".format(yesterday)
target_file_name = 'TF0G0318jp01_'+ yesterday_format +'.csv'

# 対象ファイルコピー/移動 #
shutil.copy('\\\\APLQDTExxxxxxxxxx\TF0G0318jp01\\'+ target_file_name, '試験計画_Arranged.csv')

# CSV ファイルの読み込み
with open('試験計画_Arranged.csv', 'r', encoding="utf-8") as f:
    for row in csv.DictReader(f, keys):
        json_list.append(row)

# JSON ファイルへの書き込み
with codecs.open('output.json', 'w', 'utf-8') as f:
    json.dump(json_list, f, indent=2, ensure_ascii=False)

# JSONファイルのロード
with open('output.json', 'r', encoding="utf-8") as f:
    json_PSSdata = json.load(f)
#####################################################################


#トークン取得#########################################################
url = 'https://accounts.accesscontrol.windows.net/d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8/tokens/OAuth/2'
data = {
    'grant_type':'client_credentials',
    'client_id':'<ここにクライアントIDを入力>@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8',
    'client_secret':'<ここにクライアントシークレットを入力>',
    'resource':'00000003-0000-0ff1-ce00-000000000000/toyotajp.sharepoint.com@d1c1335e-f582-42a9-b6fe-5e1a16eb9bc8',
}
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
}

t = requests.post(url, data=data, headers=headers)
json_token = json.loads(t.text)
#####################################################################


#リストアイテム検索 & 作成/更新#########################################
for i in range(1, len(json_PSSdata)):
    headers = {
        'Authorization': 'Bearer ' + json_token['access_token'],
        'Accept': 'application/json;odata=verbose',
    }
    url = "https://toyotajp.sharepoint.com/sites/<ここに対象のSPOサイト名を入力>/_api/web/lists/GetByTitle('<ここにリスト名を入力>')/items?$filter=OData__x66f8__x985e_ID eq "+ json_PSSdata[i]['OData__x66f8__x985e_ID'] +"&$select=OData__x66f8__x985e_ID,ID"
    m = requests.get(url, headers=headers)
    # print('---------ココから中身---------')
    # print(m.text)
    pickup_data = json.loads(m.text)

    strjson_PSSdata =  json.dumps(json_PSSdata[i], indent=2, ensure_ascii=False)
    strjson_PSSdata = strjson_PSSdata.lstrip('{')
    strjson_PSSdata = strjson_PSSdata.rstrip('}')
    strjson_PSSdata = strjson_PSSdata.replace('""', 'null')

    data = ('''{
        "__metadata": {
            "type": "<ここに内部リスト名を入力>"
        },
    '''+ strjson_PSSdata +'''    
    }''').encode('utf-8')

    l = requests.post(url, data=data, headers=headers)

        ###########################################################################
    if len(pickup_data['d']['results']) == 0:   ### リストに存在しない場合、新規作成 #
        ###########################################################################
        url = "https://toyotajp.sharepoint.com/sites/<ここに対象のSPOサイト名を入力>/_api/web/lists/GetByTitle('<ここにリスト名を入力>')/items"
        headers = {
            'Authorization': 'Bearer ' + json_token['access_token'],
            'Accept':'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose',
            'Content-Length': str(len(data)),
        }
        
        l = requests.post(url, data=data, headers=headers)
        # print(l.text)
        ###########################################################################
    else:                                       ###リストに存在する場合、更新 #
        ###########################################################################
        url = "https://toyotajp.sharepoint.com/sites/<ここに対象のSPOサイト名を入力>/_api/web/lists/GetByTitle('<ここにリスト名を入力>')/items("+ str(pickup_data['d']['results'][0]['ID']) +")"
        headers = {
            'Authorization': 'Bearer ' + json_token['access_token'],
            'Accept':'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose',
            'Content-Length': str(len(data)),
            'If-Match': '*',
            'X-HTTP-Method': 'MERGE'
        }

        l = requests.post(url, data=data, headers=headers)
        # print(l.text)
    print(i)

#####################################################################