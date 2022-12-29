import json

def get_ids_standard():
    '''Get post ids from a json file from The Standard news feed
    
    Args:
    Return:
        A list of ids retrieved from feed
    '''
    with open("standard_feed.json") as file:
        data = json.load(file)  
    ids = []
    for item in data['entries']:
        ids.append(item["id"])
    return ids


def get_ids_twitter():
    '''get post ids from a json file from twitter api
    
    Args:
    Return:
        None
    '''
    ids = []
    with open("tweets.json") as file:
        data = json.load(file)
    for item in data["data"]:
        ids.append(item["id"])
    return ids
    

def update_ids(list_ids):
    '''Save or update a list of IDs into a json file

    Args:
        list_ids: a list of IDs

    return:
        None
    '''
    
    with open("ids.json","r") as file:
        data = json.load(file)

    ids = data['data']
    ids.extend(list_ids)
    ids = list(set(ids))
    new_data = {"data": ids }

    with open("ids.json", "w") as file:
        file.write(json.dumps(new_data))
    return None


def save_posted_ids(list_ids):
    '''Save posted ids in a json file.
    
    Args:
        list_ids: A list of ids that have been posted
    
    Returns:
        None
    '''
    with open("posted_ids.json", "r") as file:
        data = json.load(file)

    posted_ids = data['data']
    posted_ids.extend(list_ids)
    posted_ids = list(set(posted_ids))
    posted_ids_dict = {"data":posted_ids}

    with open("posted_ids.json", "w") as file:
        file.write(json.dumps(posted_ids_dict))


def get_pending_ids():
    '''Find IDs that have not been posted

    Args:

    Returns:
        A list of IDs
    '''

    with open("ids.json") as file:
        data = json.load(file)
    ids_set = set(data['data'])  

    with open("posted_ids.json") as file:
        data = json.load(file)
    posted_ids_set = set(data['data'])

    pending_ids = ids_set - posted_ids_set
    return list(pending_ids)
