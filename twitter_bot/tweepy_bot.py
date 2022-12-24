import tweepy
import json

import requests

def send_message(text_message):
    payload = {
    "chat_id":"-1001860660149",
    "text":f"{text_message}",
    }
    url ="https://api.telegram.org/bot5927824100:AAFO2X08IzdO5uNRdRSuMr3wYBre4vWX1xo/sendMessage"
    result = requests.get(url, params=payload)
    return None




file_object = open('bearer_token.json')
data = json.load(file_object)
file_object.close()
bearer_token = data["bearer_token"]

client = tweepy.Client(bearer_token)

user_id = 22910295
response = client.get_users_tweets(user_id)

print(response.data)
print(type(response.data[0]))


for tweet in response.data:
    send_message(tweet)
    # print(tweet)
# chelsea_tweets_json = tweets.json

# with open("chelsea_tweets.txt", "w") as chelsea_tweets:
#     chelsea_tweets.write(myresponse)