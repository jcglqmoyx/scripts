import pprint

import jieba
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 发起xml请求
url = 'https://comment.bilibili.com/97509676.xml'  # 弹幕地址
html = requests.get(url).content  # 发起请求并获得网页内容
html_data = str(html, 'utf-8')  # 对网页进行‘utf-8’解码

# 解析xml并提取弹幕内容
soup = BeautifulSoup(html_data, 'lxml')
results = soup.find_all('d')  # 找到所有的‘d'标签
comments = [x.text for x in results]  # 提取每个’d'标签的text内容，即弹幕文字
pprint.pprint(comments)
# 保存结果
comments_dict = {'comments': comments[1:]}
df = pd.DataFrame(comments_dict)
df.to_csv('bilibili.csv', encoding='utf-8')

import wordcloud

# txt ="life is short,you need python"
txt = ''
for comment in comments:
    txt += comment + ' '


seg_list = jieba.cut(txt, use_paddle=True)
txt = ' '.join(list(seg_list))
print("Paddle Mode: " + '/'.join(list(seg_list)))


w = wordcloud.WordCloud(
    background_color="white",
    font_path='/home/jcglqmoyx/Downloads/微软雅黑.ttf',
    height=1000,
    width=800,
)

w.generate(txt)
w.to_file("/home/jcglqmoyx/Desktop/bilibili.png")
