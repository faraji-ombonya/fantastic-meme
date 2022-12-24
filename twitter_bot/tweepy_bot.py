import tweepy
import json


def get_bearer_token():
    '''
    get bearer token from a json file
    '''
    with open("bearer_token.json") as bearer_token_file:
        data = json.load(bearer_token_file)
        return data["bearer_token"]


def get_user_id(user_name):
    pass
    

def get_tweets(user_id):
    '''
    get tweets from specified user id
    '''
    bearer_token = get_bearer_token()
    client = tweepy.Client(bearer_token)
    response = client.get_users_tweets(user_id)
    return response.data
