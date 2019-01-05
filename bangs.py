# Author : ZhangTong

import requests
import re

def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
    except Exception as e:
        print(e)

def parse(text):
    bangs = re.findall('【(.*?)】', text, re.S)[:-1]
    return bangs

def save(content):
    fp = 'bangs.txt'
    with open(fp, 'a', encoding='utf-8') as f:
        for bangs in content:
            f.write(bangs + '\t')

def main():
    url = 'https://zhidao.baidu.com/question/67285990'
    text = download(url)
    bangs = parse(text)
    save(bangs)
if __name__ == '__main__':
    main()