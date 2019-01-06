# Author : ZhangTong
import re
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# # 画图正常显示中文
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
# # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False
# # 用来正常显示负号
def heroine():
    actress_data = {
        '赵敏': 1243,
        '周芷若': 822,
        '小昭': 354,
        '蛛儿': 231,
        '朱九真': 141,
        '杨不悔': 190
    }
    for a, b in actress_data.items():
        plt.text(a, b + 0.05, '%.0f' % b,
                 ha='center', va='bottom', fontsize=12)
        # ha 文字指定在柱体中间
        # va 指定文字位置
        # fontsize 指定文字大小
    # 设置x轴y轴数据，两者都可以是list或者tuple
    x_axis = tuple(actress_data.keys())
    y_axis = tuple(actress_data.values())
    plt.bar(x_axis, y_axis, color='rgbyck')
    # 如果不指定color，所有的柱体都会是一个颜色
    # b: blue   g: green     r: red  c: cyan
    # m: magenta    y: yellow   k: black    w: white
    plt.xlabel('女角色')   # 指定x轴描述信息
    plt.ylabel('小说中出现次数')   # 指定y轴描述信息
    plt.title('谁是女主角？') # 指定图标描述信息
    plt.ylim(0, 1400)   # 指定y轴的高度
    plt.show()

def get_names():
    file = 'names.txt'
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()

    novelNames = re.findall('《(.*?)》', text, re.S)
    names = re.findall('人）(.*?)《', text, re.S)
    yuenv = re.search('范蠡.*', text, re.S)
    names.append(yuenv.group())
    novels_and_names = {}
    for i in range(len(novelNames)):
        character_names = []
        name = names[i].split(' ')
        for j in name:
            character_names.append(j.strip())
        novels_and_names[novelNames[i]] = character_names
    return novels_and_names
def get_kungfu():
    fp = 'kungfu.txt'
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    kungfu = text.split(' ')[:-1]
    return kungfu
def get_bangs():
    fp = 'bangs.txt'
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    bangs = text.split('\t')[:-1]
    return bangs
def get_novle_text(novel_name):
    fp = '%s\%s.txt' % (novel_name, novel_name)
    with open(fp, 'r', encoding='utf-8') as f:
        novel_text = f.read()
    return novel_text

def maincharacters(novel_name):
    '''
    寻找小说中出现次数最多的人物
    :param novel_name:
    :return:
    '''
    novels_and_names = get_names()
    novel_text = get_novle_text(novel_name)
    names = novels_and_names[novel_name]
    num = 10
    count = []
    for name in names:
        count.append([name, novel_text.count(name)])
    count.sort(key=lambda x: x[1])
    _, ax = plt.subplots()
    numbers = [x[1] for x in count[-num:]]
    names = [x[0] for x in count[-num:]]
    ax.barh(range(num), numbers, align='center')
    ax.set_title(novel_name, fontsize=14)
    ax.set_yticks(range(num))
    ax.set_yticklabels(names, fontsize=10)
    plt.show()

def most_kungfu(novel_name):
    '''
    寻找小说中出现最多的武功秘籍
    :param novel_name:
    :return:
    '''
    kungfus = get_kungfu()
    novel_text = get_novle_text(novel_name)
    num = 10
    count = []
    for kungfu in kungfus:
        count.append([kungfu, novel_text.count(kungfu)])
    count.sort(key=lambda x: x[1])
    _, ax = plt.subplots()
    numbers = [x[1] for x in count[-num:]]
    kungfu = [x[0] for x in count[-num:]]
    ax.barh(range(num), numbers, align='center')
    ax.set_title(novel_name, fontsize=14)
    ax.set_yticks(range(num))
    ax.set_yticklabels(kungfu, fontsize=12)
    plt.show()

def most_bangs(novel_name):
    '''
    寻找小说中出现最多的门派
    :param novel_name:
    :return:
    '''
    bangs = get_bangs()
    novel_text = get_novle_text(novel_name)
    num = 10
    count = []
    for bang in bangs:
        count.append([bang, novel_text.count(bang)])
    count.sort(key=lambda x: x[1])
    _, ax = plt.subplots()
    numbers = [x[1] for x in count[-num:]]
    bangs = [x[0] for x in count[-num:]]
    ax.barh(range(num), numbers, align='center')
    ax.set_title(novel_name, fontsize=14)
    ax.set_yticks(range(num))
    ax.set_yticklabels(bangs, fontsize=12)
    plt.show()

def main(novel_name):
    maincharacters(novel_name)
    most_kungfu(novel_name)
    most_bangs(novel_name)

if __name__ == '__main__':
    novel_names = ['书剑恩仇录', '侠客行', '倚天屠龙记', '天龙八部', '射雕英雄传', '白马啸西风', '碧血剑', '神雕侠侣', '笑傲江湖', '越女剑', '连城诀', '雪山飞狐', '飞狐外传', '鸳鸯刀', '鹿鼎记']
    print('请选择你想查看的小说编号:')
    for i in range(len(novel_names)):
        print('%d \t %s' % (i+1, novel_names[i]))
    num = int(input())
    novel_name = novel_names[num]
    main(novel_name)








