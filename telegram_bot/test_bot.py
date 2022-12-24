import requests
import json

def send_message(text_message):
    payload = {
    "chat_id":"-1001860660149",
    "text":f"{text_message}",
    }

    with open("api_key.json") as api_key_file:
        data = json.load(api_key_file)
        api_key = data['api_key']

    url ="https://api.telegram.org/bot{}/sendMessage".format(api_key)
    requests.get(url, params=payload)
    return None

