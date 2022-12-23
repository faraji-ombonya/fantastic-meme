import requests

def send_message(text_message):
    payload = {
    "chat_id":"-1001860660149",
    "text":f"{text_message}",
    }
    url ="https://api.telegram.org/bot5927824100:AAFO2X08IzdO5uNRdRSuMr3wYBre4vWX1xo/sendMessage"
    result = requests.get(url, params=payload)
    return None

my_message = "HI, testing with a function"
send_message(my_message)