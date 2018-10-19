url_attack = 'http://data.champdas.com/person/rank/attack.html'
url_pass = 'http://data.champdas.com/person/rank/pass.html'
url_defend = 'http://data.champdas.com/person/rank/defend.html'
url_overall = 'http://data.champdas.com/person/rank/overall.html'
# ============================================================
# =============== overall
# ============================================================




# ============================================================
# =============== Dict
# ============================================================
totalsize = {
    '2014': 412,
    '2015': 427,
    '2016': 416,
    '2017': 430,
    '2018': 324
}
offsize = {
    '2014': 43,
    '2015': 44,
    '2016': 43,
    '2017': 44,
    '2018': 33
}
# ============================================================
# =============== attack
# ============================================================
import requests
import json
import time
import random
myheader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
form_attack = {
    'leagueId':1,
   # 'season':2014,
    'orderType':6,
   # 'offset':38,
   # 'totalSize':412,
    'personType':1,
    'dataType':2
}
attack_dict = {
    '2014':[],
    '2015':[],
    '2016':[],
    '2017':[],
    '2018':[]
}
url_attack = 'http://data.champdas.com/person/rank/attack.html'
for i in range(2014,2019):
    form_attack['season'] = i
    res = requests.post(url_attack, headers=myheader, data=form_attack)
    time.sleep(random.choice(range(3,6)))
    attack = json.loads(res.text)[0]
    attack_dict[str(i)] = attack_dict[str(i)] + attack
    print('球员攻击数据: {}年第【1】页获取成功!'.format(i))
    form_data = form_attack
    form_data['totalSize'] = totalsize['{}'.format(i)]
    for j in range(2,offsize['{}'.format(i)]):
        form_data['offset'] = j
        res = requests.post(url_attack, headers=myheader, data=form_data)
        time.sleep(random.choice(range(3,5)))
        attack = json.loads(res.text)[0]
        attack_dict[str(i)] = attack_dict[str(i)] + attack
        print('球员攻击数据: {0}年第【{1}】页获取成功!'.format(i,j))
import pandas as pd
attack_dict_all={}
for year in attack_dict.keys():
    for key in attack_dict[year][0].keys():
        attack_dict_all[key] = []
attack_dict_all['Season']=[]
for year in attack_dict.keys():
    for attack in attack_dict[year]:
        attack['Season'] = year
        for key, value in attack.items():
            attack_dict_all[key].append(value)
attack_df = pd.DataFrame(attack_dict_all)
attack_df.to_csv('attack.csv',encoding='utf8')
# ============================================================
# =============== pass
# ============================================================
form_pass = {
    'leagueId':1,
    #'season':2014,
    'orderType':16,
    #'offset':38,
    #'totalSize':412,
    'personType':1,
    'dataType':2
}
pass_dict = {
    '2014':[],
    '2015':[],
    '2016':[],
    '2017':[],
    '2018':[]
}
url_pass = 'http://data.champdas.com/person/rank/pass.html'
for i in range(2014,2019):
    form_pass['season'] = i
    res = requests.post(url_pass, headers=myheader, data=form_pass)
    time.sleep(random.choice(range(3,5)))
    passdata = json.loads(res.text)[0]
    pass_dict[str(i)] = pass_dict[str(i)] + passdata
    print('球员传球数据: {}年第【1】页获取成功!'.format(i))
    form_data = form_pass
    form_data['totalSize'] = totalsize['{}'.format(i)]
    for j in range(2, offsize['{}'.format(i)]):
        form_pass['offset'] = j
        res = requests.post(url_pass, headers=myheader, data=form_data)
        time.sleep(random.choice(range(3,6)))
        passdata = json.loads(res.text)[0]
        pass_dict[str(i)] = pass_dict[str(i)] + passdata
        print('球员传球数据: {0}年第【{1}】页获取成功!'.format(i,j))
import pandas as pd
pass_dict_all={}
for year in pass_dict.keys():
    for key in pass_dict[year][0].keys():
        pass_dict_all[key] = []
pass_dict_all['Season']=[]
for year in pass_dict.keys():
    for passdata in pass_dict[year]:
        passdata['Season'] = year
        for key, value in passdata.items():
            pass_dict_all[key].append(value)
pass_df = pd.DataFrame(pass_dict_all)
pass_df.to_csv('pass.csv',encoding='utf8')

# ============================================================
# =============== defend
# ============================================================
form_defend = {
    'leagueId':1,
    #'season':2014,
    'orderType':11,
    #'offset':38,
    #'totalSize':412,
    'personType':1,
    'dataType':2
}
defend_dict = {
    '2014':[],
    '2015':[],
    '2016':[],
    '2017':[],
    '2018':[]
}
url_defend = 'http://data.champdas.com/person/rank/defend.html'
for i in range(2014,2019):
    form_defend['season'] = i
    res = requests.post(url_defend, headers=myheader, data=form_defend)
    time.sleep(random.choice(range(5,7)))
    defend = json.loads(res.text)[0]
    defend_dict[str(i)] = defend_dict[str(i)] + defend
    print('球员防守数据: {}年第【1】页获取成功!'.format(i))
    form_data = form_defend
    form_data['totalSize'] = totalsize['{}'.format(i)]
    for j in range(2, offsize['{}'.format(i)]):
        form_defend['offset'] = j
        res = requests.post(url_defend, headers=myheader, data=form_data)
        time.sleep(random.choice(range(5,7)))
        defend = json.loads(res.text)[0]
        defend_dict[str(i)] = defend_dict[str(i)] + defend
        print('球员防守数据: {0}年第【{1}】页获取成功!'.format(i,j))
import pandas as pd
defend_dict_all={}
for year in defend_dict.keys():
    for key in defend_dict[year][0].keys():
        defend_dict_all[key] = []
defend_dict_all['Season']=[]
for year in defend_dict.keys():
    for defend in defend_dict[year]:
        defend['Season'] = year
        for key, value in defend.items():
            defend_dict_all[key].append(value)
defend_df = pd.DataFrame(defend_dict_all)
defend_df.to_csv('defend.csv',encoding='utf8')
# ============================================================
# =============== overall
# ============================================================
form_overall = {
    'leagueId':1,
    #'season':2014,
    'orderType':1,
    #'offset':38,
    #'totalSize':412,
    'personType':1,
    'dataType':2
}
overall_dict = {
    '2014':[],
    '2015':[],
    '2016':[],
    '2017':[],
    '2018':[]
}
url_overall = 'http://data.champdas.com/person/rank/overall.html'
for i in range(2014,2019):
    form_overall['season'] = i
    res = requests.post(url_overall, headers=myheader, data=form_overall)
    time.sleep(random.choice(range(4,6)))
    overall = json.loads(res.text)[0]
    overall_dict[str(i)] = overall_dict[str(i)] + overall
    print('球员总体数据: {}年第【1】页获取成功!'.format(i))
    form_data = form_overall
    form_data['totalSize'] = totalsize['{}'.format(i)]
    for j in range(2, offsize['{}'.format(i)]):
        form_defend['offset'] = j
        res = requests.post(url_overall, headers=myheader, data=form_data)
        time.sleep(random.choice(range(4,6)))
        overall = json.loads(res.text)[0]
        overall_dict[str(i)] = overall_dict[str(i)] + overall
        print('球员总体数据: {0}年第【{1}】页获取成功!'.format(i,j))
import pandas as pd
overall_dict_all={}
for year in overall_dict.keys():
    for key in overall_dict[year][0].keys():
        overall_dict_all[key] = []
overall_dict_all['Season']=[]
for year in overall_dict.keys():
    for overall in overall_dict[year]:
        overall['Season'] = year
        for key, value in overall.items():
            overall_dict_all[key].append(value)
overall_df = pd.DataFrame(overall_dict_all)
overall_df.to_csv('overall.csv',encoding='utf8')













