import requests
import base64
from pprint import pprint
from bs4 import BeautifulSoup

from spider.models import Post
from spider.utils.telegram import Telegram

class Star():
    def __init__(self):
        pass

    def get_entries(self):
        url = 'https://www.the-star.co.ke/sports/football/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # entrys = soup.find_all('div', class_='thing')
        # print(soup.find_all('div','section-article'))

        articles = soup.find_all('div', 'section-article')
        base = "https://www.the-star.co.ke"

        entries = []
        for article in articles:
            entry = {}

            entry['source'] = "The Star"

            # entry['description'] = article.find('p').contents[0]
            # entry['link_title'] = article.find('a').get("title")
            # article card title
            

            # title
            entry['title'] = None
            title = article.find('h3')
            if title:
                entry['title'] = title.contents[0]
            
            # link
            entry['link'] = None
            article_link = article.find('a').get("href")
            if article_link:
                entry['link'] = f"{base}{article_link}"

            # synopsis
            entry['synopsis'] = None
            article_synopsis = article.find('p', 'article-synopsis')
            if article_synopsis:
                entry['synopsis'] = article_synopsis.contents[0]

            # author
            entry['author'] = None
            span_article_author = article.find('span', 'article-author')
            if span_article_author:
                author = span_article_author.contents[0]
                if author:
                    entry['author'] = span_article_author.contents[0]
                    author_span_link = span_article_author.a
                    if author_span_link:
                        entry['author'] = author_span_link.contents[0]

            # category
            entry['category'] = None
            article_section = article.find('span', 'article-section')
            if article_section:
                article_section_a = article_section.a
                if article_section_a:
                    entry['category'] = article_section_a.contents[0]

            entries.append(entry)
            pprint(entry)
            print()

      
        return entries
   
    def _extract_image_from_style(self, style):
        start_index = style.find("url(")
        end_index = style.find(");", start_index)
        if start_index != -1 and end_index != -1:
            link_style_image = style[start_index + 4:end_index].strip("'\" ")
            return link_style_image
        

    def get_posts(self, entries):
        if entries:
            posts = []
            for entry in entries:
                post = {}
                post['slug'] = entry.get('link')
                post['content'] = entry

                posts.insert(0, post)

            print(posts)
            return posts

    def save_posts(self, posts):
        if posts:
            Post.objects.bulk_create(
                [Post(**post) for post in posts],
                ignore_conflicts=True)
            
    def transform_star_telegram(self, post):
        content = post.content
        title = content.get('title')
        link = content.get('link')
        summary = content.get('synopsis')
        author = content.get('author')
        category = content.get('category')
        source = content.get('source')

        return f"{title}\n{link}\n{summary}\n[{source} | {author} | {category}]"
    