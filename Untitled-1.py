import requests
import json

webhook_url = "https://prod-73.westus.logic.azure.com:443/workflows/1b12f9eab547427cba9ce839aedc6f9d/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=-CtSG3GpaLPzTw5jr3wJqVIAVe1gnDaydjMci-Kr8NA"
message = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Raspberry Pi からのメッセージです！"
                    }
                ]
            }
        }
    ]
}

response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, json=message)
print(response.status_code)
