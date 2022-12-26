import tweepy
import json


def get_bearer_token():
    '''
    get bearer token from a json file
    '''
    with open("storage/bearer_token.json") as bearer_token_file:
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
    response = client.get_users_tweets(user_id, exclude="retweets")
    return response.data


def update_ids(list_ids):
    '''
    Updates tweet ids in a json file
    '''
    with open("storage/ids.json", "r") as file:
        data = json.load(file)

    existing_list_ids = data['data']
    existing_list_ids.extend(list_ids)
    existing_list_ids = list(set(existing_list_ids))

    new_dict = {"data": existing_list_ids}
    json_string = json.dumps(new_dict)

    with open("storage/ids.json", "w") as file:
        file.write(json_string)


def save_posted_ids(list_ids):
    '''
    save posted ids in a json file
    '''

    with open("storage/posted_ids.json", "r") as file:
        data = json.load(file)

    posted_ids = data['data']
    posted_ids.extend(list_ids)
    posted_ids = list(set(posted_ids))

    posted_ids_dict = {
        "data":posted_ids
    }

    posted_ids_json = json.dumps(posted_ids_dict)

    with open("storage/posted_ids.json", "w") as file:
        file.write(posted_ids_json)


def get_pending_ids():
    '''
    find and return a list of ids that have not been posted yet
    '''

    with open("storage/ids.json") as file:
        data = json.load(file)
    ids_set = set(data['data'])  

    with open("storage/posted_ids.json") as file:
        data = json.load(file)
    posted_ids_set = set(data['data'])

    pending_ids = ids_set - posted_ids_set

    return list(pending_ids)