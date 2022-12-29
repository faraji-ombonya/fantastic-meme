import requests
import json

def send_message(text_message, chat_id="-1001860660149"):
    '''Send message to a telegram channel
    
    Args:
        text_message: message to send
        chat_id: chat id if the channel

    Return:
        None
    '''
    payload = {
    "chat_id": chat_id,
    "text": f"{text_message}",
    }

    with open("api_key.json") as api_key_file:
        data = json.load(api_key_file)
        api_key = data['api_key']

    url ="https://api.telegram.org/bot{}/sendMessage".format(api_key)
    requests.get(url, params=payload)
    return None
