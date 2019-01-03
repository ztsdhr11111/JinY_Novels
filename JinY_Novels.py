# Author : ZhangTong

import requests
import re
import time
import os
from bs4 import BeautifulSoup
from lxml import etree

def structure_section(url):
    '''
    对有小节的章节链接进行重构
    :param url:
    :return:
    '''
    urls = []
    text = download(url)
    html = etree.HTML(text)
    try:
        if html.xpath('//div[@class="apnavi"]'):
            last = int(html.xpath('//div[@class="apnavi"]/a/span/text()')[-1])
            for i in range(1, last+1):
                urls.append(url + '/%s/' % i)
            return urls
        else:
            urls.append(url)
            return urls
    except Exception as e:
        print(e, url)

def download(url):
    '''
    发送请求，返回响应内容
    :param url:
    :return:
    '''
    headers = {
        "Host": 'www.luoxia.com',
        "Cookie": '__cfduid=d6ff9743329e347587e5eac28214a92e11546492773; _ga=GA1.2.1065230300.1546492779; _gid=GA1.2.1091847329.1546492779; _gat_gtag_UA_16539659_3=1',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'UTF-8'
        return response.text
    pass

def parse_index(text):
    '''
    解析索引页面，得到每个小说的链接
    :param text:
    :return:
    '''
    item = {}
    soup = BeautifulSoup(text, 'lxml')
    tt = soup.select('.pop-book2')
    for i in tt:
        title = i.select('.pop-tit')[0].string
        href = i.select('a')[0]['href']
        item[title] = href
    return item

def parse_section(text):
    '''
    获取每本小说的每个章节链接
    :param text:
    :return:
    '''
    novel = {}
    html = etree.HTML(text)
    section = html.xpath('//div[@class="book-list clearfix"]/ul/li/a/text() | //div[@class="book-list clearfix"]/ul/li/b/text()')
    href = html.xpath('//div[@class="book-list clearfix"]/ul/li/a/@href | //div[@class="book-list clearfix"]/ul/li/b/@onclick')
    for i in range(len(section)):
        href[i] = re.search('http.*?htm', href[i], re.S).group()
        href[i] = structure_section(href[i])
        novel[section[i]] = href[i]
    return novel

def parse_section_content(text):
    '''
    获取小说内容
    :param text:
    :return:
    '''
    html = etree.HTML(text)
    contents = html.xpath('//div[@id="nr1"]/p/text()')
    content = '\n'.join(contents)
    return content

def save(novel_title, novel_section, content):
    '''
    保存文件
    :param novel_title:
    :param novel_section:
    :param content:
    :return:
    '''
    fp = r'%s\%s.txt' % (novel_title, novel_title)
    if not os.path.exists(novel_title):
        os.mkdir(novel_title)
    with open(fp, 'a', encoding='utf-8') as f:
        f.write(novel_section + '\n')
        f.write(content)

def first_step():
    url = 'http://www.luoxia.com/jinyong/'
    index_text = download(url)
    item = parse_index(index_text)
    for novel_title, novel_link in item.items():
        yield novel_title, novel_link

def second_step(url):
    section_text = download(url)
    sections = parse_section(section_text)
    return sections

def thread_step(link):
    contents = []
    for url in link:
        text = download(url)
        content = parse_section_content(text)
        contents.append(content)
    contents = '\n'.join(contents)
    return contents

def main():
    for novel_title, novel_link in first_step():
        print('%s:%s' % (novel_title, novel_link))
        sections = second_step(novel_link)
        for sec, link in sections.items():
            print('%s: %s' % (sec, link))
            content = thread_step(link)
            save(novel_title, sec, content)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('Total Spend Tiem: %s' % (end-start))