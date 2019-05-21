#encoding:utf-8

import requests
import re
import pandas as pd

url_first = 'https://movie.douban.com/subject/26363254/comments?start=0'

# find the coresponding cookies
head = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36'}
html = requests.get(url_first, headers=head, cookies=cookies)
cookies = {'cookie':''} # cookies corresponding to your account

reg=re.compile(r'<a href="(.*?)&amp;.*?class="next">') # next page
ren=re.compile(r'<span class="votes">(.*?)</span>.*?comment">(.*?)</a>.*?</span>.*?<span.*?class="">(.*?)</a>.*?<span>(.*?)</span>.*?title="(.*?)"></span>.*?title="(.*?)">.*?class=""> (.*?) ',re.S) # review content

while html.status_code==200:
    url_next='https://movie.douban.com/subject/26363254/comments'+re.findall(reg,html.text)[0]
    zhanlang=re.findall(ren,html.text)

data = pd.DataFrame(zhanlang)
data.to_csv('/home/wajuejiprince/文档/zhanlang/zhanlangpinglun.csv', header=False,index=False,mode='a+')
data = []
zhanlang = []
html = requests.get(url_next, cookies=cookies, headers=head)
