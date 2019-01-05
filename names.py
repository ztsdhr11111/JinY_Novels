# Author : ZhangTong

import requests
from lxml import etree

def sturcture():
    base_url = 'http://blog.renren.com/share/276672925/14420802871/'
    urls = [base_url + str(i) for i in range(3)]
    return urls

def download(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'UTF-8'
            return response.text
    except Exception as e:
        print(e)

def parse(text):
    html = etree.HTML(text)
    names = [i.strip() for i in html.xpath('//div[@class="content-body"]/text()')][2:-1]
    return names

def save(content):
    fp = 'names.txt'
    with open(fp, 'a', encoding='utf-8') as f:
        for i in content:
            f.write(i)

def main(url):
    text = download(url)
    content = parse(text)
    save(content)

if __name__ == '__main__':
    urls = sturcture()
    for url in urls:
        main(url)