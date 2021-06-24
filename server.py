import time
import requests
import re
from bs4 import BeautifulSoup
from NCMB.Client import NCMB
import config

ncmb = NCMB(config.application_key, config.client_key)


def get_data():
    query = ncmb.Query('Tenpo')
    result = query.equal_to('Sheets', 18).fetch_all()
    print(result[0].get('TenpoName'))

def set_news_data(title, url):
    obj = ncmb.Object('News')
    obj.set(
            'Title', title
       ).set(
            'URL', url
       ).save()


def get_yahoo_news(keywords):
    url = 'https://www.yahoo.co.jp/'
    content = requests.get(url)

    soup = BeautifulSoup(content.text, 'html.parser')

    news_list = soup.find_all(href=re.compile('news.yahoo.co.jp/pickup'))
    corona_news_list = []
    for news in news_list:
        for keyword in keywords:
            if keyword in news.span.string:
                corona_news_list.append({
                        'Title' : news.span.string,
                        'URL' : news.attrs['href']
                    })
                break

    for news in corona_news_list:
        print(news['Title'])
        print(news['URL'])

    return corona_news_list


def read_keywords(filename):
    words = []
    with open(filename, encoding='utf-8') as f:
        words = f.readlines()
    return [word.replace('\n', '') for word in words]


def main():
    keywords_filename = './keywords.txt'
    keywords = read_keywords(keywords_filename)
    print(keywords)

    while True:
        news_list = get_yahoo_news(keywords)
        for news in news_list:
            set_news_data(news['Title'], news['URL'])
        time.sleep(600)


if __name__ == '__main__':
    main()
