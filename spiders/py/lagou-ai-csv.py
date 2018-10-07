
# coding: utf-8

# ### 读取一个文件

# In[16]:


def range2two(s, unit):
    s = s.replace(unit, '')  #去掉单位k、年、人
    s = s.replace(' ', '')  #去掉空格
    l = s.split('-')
    res = {
        'low': str(l[0]),
        'high': str(l[1]) if len(l) > 1 else 'None'
    }
    return res


# In[25]:


import json
labels = [
    'positionId', 'positionName', 'workYear', 'education', 'createTime',
    'salary', 'city', 'companyFullName', 'companySize', 'financeStage',
    'firstType', 'secondType', 'details'
]
labels2 = [
    'salary_low', 'salary_high', 'workYear_low', 'workYear_high',
    'companySize_low', 'companySize_high'
]


def readJob(fileName):
    with open(fileName, 'r') as f:
        job = json.load(f)
        line = []
        for key in labels:
            line.append(str(job[key]).replace(',','，'))  #添加所有labels的字段，用中文逗号替换英文逗号，避免分割混乱

        salaries = range2two(job['salary'], 'k')
        workYears = range2two(job['workYear'], '年')
        companySizes = range2two(job['companySize'], '人')
        line += [salaries['low'], salaries['high']]
        line += [workYears['low'], workYears['high']]
        line += [companySizes['low'], companySizes['high']]

        return ','.join(line)


# In[37]:


import os
files = os.listdir('./data/lagou_ai/jobs/')  #获取所有文件列表
with open('./data/lagou_ai/jobs.csv', 'w', encoding="gb18030") as f:
    text = ''
    text += ','.join(labels + labels2)

    for fname in files:
        if not fname.find('.json')==-1:
            text += '\n'
            text += readJob('./data/lagou_ai/jobs/' + fname)
    f.write(text)
    f.close()
    print('>>OK!')

