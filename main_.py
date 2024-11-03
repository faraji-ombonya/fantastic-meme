import twitter_bot.tweepy_bot as tp
import twitter_bot.tweety as tt
import telegram.bot as tg
import json
import standard.content as st
import ids.handle_ids as h


def send_twitter_updates():
    user_id = 22910295
    tweets = tp.get_tweets(user_id)

    tweet_ids = []
    for tweet in tweets:
        tweet_ids.append(tweet.id)

    tp.update_ids(tweet_ids)

    pending_ids_list = tp.get_pending_ids()

    if len(pending_ids_list):
        url = tt.create_url(pending_ids_list)
        json_response = tt.connnect_to_endpoint(url)
        with open("new_tweets.json","w+") as tweets_json_file:
            tweets_json_file.write(json.dumps(json_response, indent=4, sort_keys=True))

        with open("new_tweets.json") as file:
            data = json.load(file)

            for item in data["data"]:
                try: 
                    expanded_url = item["entities"]["urls"][0]["expanded_url"]
                except:
                    continue
                tg.send_message(expanded_url)
        tp.save_posted_ids(pending_ids_list)


def send_standard_updates():
    st.fetch_content_standard()
    ids = h.get_ids_standard()
    h.update_ids(ids)
    pending_ids = h.get_pending_ids()

    if len(pending_ids):
        posts = st.get_posts(pending_ids)

        for item in posts:
            tg.send_message(item)
            # print(item)

        h.save_posted_ids(pending_ids)
    return None

send_standard_updates()
