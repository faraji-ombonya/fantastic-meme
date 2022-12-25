import telegram_bot.test_bot as tg
import json


with open("new_tweets.json") as file:
    data = json.load(file)
    expanded_url = data["data"][0]["entities"]["urls"][0]["expanded_url"]






tg.send_message(expanded_url)