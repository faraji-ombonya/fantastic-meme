import requests
from pprint import pprint
from bs4 import BeautifulSoup

class Star():
    def __init__(self):
        pass

    def get_posts(self):
        url = 'https://www.the-star.co.ke/sports/football/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # posts = soup.find_all('div', class_='thing')
        # print(soup.find_all('div','section-article'))

        articles = soup.find_all('div', 'section-article')

        for article in articles:
            post = {}

            post['title'] = article.find('h3').string
            # post['description'] = article.find('p').contents[0]
            post['link'] = article.find('a').get("href")
            # post['link_title'] = article.find('a').get("title")
            # post['link_style'] = article.find('a').get("style")


            # synopsis
            post['synopsis'] = None
            article_synopsis = article.find('p', 'article-synopsis')
            if article_synopsis:
                post['synopsis'] = article_synopsis.contents[0]

            # author
            post['author'] = None
            span_article_author = article.find('span', 'article-author')
            if span_article_author:
                author = span_article_author.contents[0]
                if author:
                    post['author'] = span_article_author.contents[0]
                    author_span_link = span_article_author.a
                    if author_span_link:
                        post['author'] = author_span_link.contents[0]

            # article card title
            

            # post.title = article.

            # print(article.find('h3').contents[0])
            # print(article.find('p').text)
            # print(article.find('a').text)
            pprint(post)
            print()
        return
        
