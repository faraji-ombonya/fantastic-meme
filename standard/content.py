import feedparser
import json


def fetch_content_standard():
    '''Get content from standard rss feed
    
    Returns:
        None
    '''

    with open("standard_digital_rss.json") as file:
        data = json.load(file)
    sports_url = data['data']['sports']

    d = feedparser.parse(sports_url)

    with open("feed.json", "w") as file:
        file.write(json.dumps(d, indent=4, sort_keys=True ))

    return None

    

def get_posts(list_ids):
    '''Get posts with matching IDs from the list
    
    Args:
        list_ids: list of ids to fetch posts

    Return:
        A list of posts
    '''
    posts = []

    with open("feed.json") as file:
        data = json.load(file)

    for item in data['entries']:
        if item['id'] in list_ids:
            posts.append(item['link'])

    return posts