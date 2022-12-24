import requests
import os
import json

def create_url():
    user_id = "@FarajiOmbonya"
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    return{"tweet.fields":"created_at"}

def bearer_oauth():
    '''
    Method required by bearer token authentication
    '''
    r.headers