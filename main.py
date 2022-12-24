import twitter_bot.tweepy_bot as tw
import telegram_bot.test_bot as tg

user_id = 22910295
tweets = tw.get_tweets(user_id)

for tweet in tweets:
    tg.send_message(tweet)