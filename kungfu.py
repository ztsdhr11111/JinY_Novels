# Author : ZhangTong

import requests
from lxml import etree


def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except Exception as e:
        print(e)

def parse(text):
    html = etree.HTML(text)
    kungfu_lst = html.xpath('//ol[@class="sub_toc_list"]/li/a/text()')
    kungfu = list(set([i.strip() for i in kungfu_lst]))
    return kungfu


def save(content):
    fp = 'kungfu.txt'
    with open(fp, 'a', encoding='utf-8') as f:
        for i in content:
            f.write(i + ' ')

def main():
    url = 'http://www.wikiwand.com/zh-cn/%E9%87%91%E5%BA%B8%E7%AD%86%E4%B8%8B%E6%AD%A6%E5%8A%9F%E5%88%97%E8%A1%A8#/'
    text = download(url)
    kungfu = parse(text)
    save(kungfu)

if __name__ == '__main__':
    main()