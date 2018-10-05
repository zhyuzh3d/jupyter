#cell-1

url = 'https://www.jianshu.com/u/ae784c57b353'
params = {'order_by': 'shared_at', 'page': '1'}
headers = '''
GET /u/ae784c57b353 HTTP/1.1
Host: www.jianshu.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: read_mode=day; default_font=font2; locale=zh-CN; ......b9fb068=1538705012
If-None-Match: W/"31291dc679ccd08938f27b1811f8b263"
'''

#cell-2

def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')

# cell-3

import requests
from bs4 import BeautifulSoup

html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
afocus = soup.find('div', 'info').find_all('div','meta-block')[0].find('p').string
afuns = soup.find('div', 'info').find_all('div','meta-block')[1].find('p').string
acount = soup.find('div', 'info').find_all('div','meta-block')[2].find('p').string
awords = soup.find('div', 'info').find_all('div','meta-block')[3].find('p').string
alike = soup.find('div', 'info').find_all('div','meta-block')[4].find('p').string
acount=int(acount)
print('>>文章总数', acount)

#cell-4


import math
import time

aread = 0
pages = math.ceil(acount / 9)
data = []
for n in range(1, pages + 1):
    params['page'] = str(n)
    html = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    alist = soup.find_all('div', 'content')
    for item in alist:
        line = []
        titleTag = item.find('a', 'title')  #标题行a标记
        line.append(titleTag['href'])  #编号
        line.append(titleTag.string)  #标题

        read = item.find('div', 'meta').find('a').contents[2]
        aread += int(read)  #计算总阅读量
        line.append(str(int(read)))  #编号,先转int去掉空格回车，再转str才能进line

        data.append(','.join(line))
        print('已获取:', len(data))
    time.sleep(1)


#cell-5

tm = str(int(time.time()))
fname = './data/articles_' + tm + '.csv'
with open(fname, 'w', encoding="gb18030") as f:
    f.write('\n'.join(data))
    f.close()

#cell-6

from os.path import exists
alabels = ['time', 'focus', 'funs', 'articles', 'words', 'like', 'read']
adata = [tm, afocus, afuns, str(acount), awords, alike, str(aread)]
afname='./articles_total.csv'
if not exists(afname):
    with open(afname, 'a', encoding="gb18030") as f:
        f.write(','.join(alabels)+'\n')
        f.close()
with open(afname, 'a', encoding="gb18030") as f:
    f.write(','.join(adata)+'\n')
    f.close()

#cll-7

print('>>完成，保存在%s'%fname)

