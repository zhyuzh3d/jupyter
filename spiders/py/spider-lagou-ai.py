
# coding: utf-8

# ## 拉钩搜索‘人工智能’职位列表，包含二级页面详情

# ### 设置

# In[1]:


url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
params = {
    'first': 'false',
    'pn': '1',
    'kd': '人工智能',
}
savePath='./data/lagou_ai'
headers='''
POST /jobs/positionAjax.json?needAddtionalResult=false HTTP/1.1
Host: www.lagou.com
Connection: keep-alive
Origin: https://www.lagou.com
X-Anit-Forge-Code: 0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: application/json, text/javascript, */*; q=0.01
X-Requested-With: XMLHttpRequest
X-Anit-Forge-Token: None
Referer: https://www.lagou.com/jobs/list_%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD?labelWords=&fromSearch=true&suginput=
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cookie: JSESSIONID=ABAAABAAAGFABEF8929AE8AEDDF675B0A416152D50F1155; user_trace_token=20180914214240-a2c37a86-ee75-49d4-a447-7d7ec6386510; _ga=GA1.2.764376373.1536932562; LGUID=20180914214241-0d64224c-b824-11e8-b93f-5254005c3644; WEBTJ-ID=20180917170602-165e6c78d78209-0f57b07806360b-3461790f-1296000-165e6c78d7953; __utmc=14951595; __utmz=14951595.1537175176.1.1.utmcsr=m_cf_cpt_sogou_pc|utmccn=(not%20set)|utmcmd=(not%20set); X_HTTP_TOKEN=b53ce1f559f492d4aa675d08bfaa8d93; _putrc=67FE3A6CCEBE7074123F89F2B170EADC; login=true; index_location_city=%E5%85%A8%E5%9B%BD; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B75537; __utma=14951595.764376373.1536932562.1537831174.1537969747.13; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1536932564,1537493466,1537971720,1537971743; _gid=GA1.2.149871887.1538874982; LGSID=20181007091622-9a243d33-c9ce-11e8-bb68-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=search_code; SEARCH_ID=55185a7a6e294ec483df5c15b726598b; _gat=1; LGRID=20181007092755-37b31c47-c9d0-11e8-bb68-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538875676
'''


# In[2]:


#转换headers为字典
def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')


# ### 读取单个职位详情的函数

# In[3]:


from bs4 import BeautifulSoup


def readJobDetails(pid):
    html = requests.get(
        'https://www.lagou.com/jobs/' + str(pid) + '.html', headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    res = soup.find('dd', 'job_bt').text.replace('\n', '')
    return res


# ### 发起请求

# In[4]:


import json
import requests
import time

for n in range(1, 30):
    params['pn'] = n
    jsonData = requests.get(url, params=params, headers=headers)
    data = json.loads(jsonData.text)
    jobs = data['content']['positionResult']['result']
    for job in jobs:
        pid = str(job['positionId'])
        fname = savePath + '/jobs/' + pid + '.json'
        job['details'] = readJobDetails(job['positionId'])
        with open(fname, 'w') as f:
            f.write(json.dumps(job))
            f.close()
        print('>Got job:', pid)
        time.sleep(1)
    time.sleep(1)
print('>Finished!')

