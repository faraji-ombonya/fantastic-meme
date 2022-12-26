import requests
import os
import json


def create_url(list_ids):
    '''
    create url from a list of tweet ids
    '''
    ids = "ids="
    for id in list_ids:
        ids += str(id)
        if list_ids[-1] == id:
            continue
        ids += ","
    tweet_fields = "tweet.fields=entities"
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    '''
    Method required by bearer token authentication.
    '''
    with open("storage/bearer_token.json") as bearer_token_file:
        data = json.load(bearer_token_file)
        bearer_token = data["bearer_token"]

    r.headers["Authorization"]=f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connnect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned and error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()