import feedparser
import json

def get_content():
    d = feedparser.parse("storage/feed.xml")

    with open("storage/feed.json","w") as file:
        file.write(json.dumps(d, indent=4, sort_keys=True))

    with open("storage/feed.json", "r") as file:
        data = json.load(file)

    content = []
    for item in data['entries']:
        title =item['title']
        summary = item['summary']
        author = item['author']
        link = item['link']

        content.append(f"{title}\n {summary}\n {author} \n{link}")
    return content
