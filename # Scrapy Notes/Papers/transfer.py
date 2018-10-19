# =================================================================
# =============== url load
# =================================================================
import time
import random
import json
import requests
myheader = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
def get_url(start=0,length=20,begin=17,end=18, step=1523519834220):
    url = 'http://www.tzuqiu.cc/transferList/queryTransferList.json?draw=1&columns%5B0%5D%5Bdata%5D=playerFormat&columns%5B0%5D%5Bname%5D=p.nameZh&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=transferDateFormat&columns%5B1%5D%5Bname%5D=t.transferDate&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=mfClubIdFormat&columns%5B2%5D%5Bname%5D=t.mfClubName&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=miClubIdFormat&columns%5B3%5D%5Bname%5D=t.miClubName&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=marketValueFormat&columns%5B4%5D%5Bname%5D=t.marketValue&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=transferFeeFormat&columns%5B5%5D%5Bname%5D=t.transferFee&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&start={0}&length={1}&search%5Bvalue%5D=&search%5Bregex%5D=false&extra_param%5BcompetitionId%5D=3&extra_param%5BendTransferDate%5D=today&extra_param%5Bseason%5D={2}%2F{3}&_={4}'.\
        format(start, length, begin, end, step)
    return url
def get_record(url):
    res = requests.get(url, headers = myheader)
    res.encoding = 'urf8'
    record = json.loads(res.text)['recordsTotal']
    return record
def get_data(url):
    res = requests.get(url, headers=myheader)
    data = json.loads(res.text)['data']
    return data
tran_data = {}
record_list = []
# ============================================================
# =============== data load
# ============================================================
for i in range(11,18):
    url = get_url(begin = i, end= i+1)
    rec = get_record(url)
    record_list.append(rec)
for i in range(11,18):
    url = get_url(length=record_list[i-11],begin = i, end = i+1)
    data = get_data(url)
    time.sleep(random.choice(range(3)))
    tran_data['{}'.format(i)] = data
for i in range(11,18):
    print(len(tran_data['{}'.format(i)]))
# ============================================================
# =============== data output
# ============================================================
tran_dict = {}
tran_dict['year'] = []
for key in tran_data['{}'.format(11)][0].keys():
    tran_dict[key] = []
for i in range(11,18):
    for tran in tran_data['{}'.format(i)]:
        for key, value in tran.items():
            tran_dict[key].append(value)
        tran_dict['year'].append(i)
for key in tran_dict.keys():
    print(key,len(tran_dict[key]))
for key in tran_dict.keys():
    leng = len(tran_dict[key])
    if not leng == 2392:
        print(key)
import pandas as pd
tran_df = pd.DataFrame(tran_dict)
tran_df.to_csv('tran_df.csv',encoding='utf8')


