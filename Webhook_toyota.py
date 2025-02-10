import requests
import json
webhook_url = "https://prod-08.japaneast.logic.azure.com:443/workflows/e529f73cbde0496d9659c20cb518c199/triggers/manual/paths/invoke?api-version=2016-06-01"
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
                        "text": "testメッセージ"
                    }
                ]
            }
        }
    ]
}

response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, json=message)
print(response.status_code)

