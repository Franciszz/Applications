import requests
import wechatsogou
### 连接

ws_api = wechatsogou.WechatSogouAPI()

### 验证码输入次数

ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

### 设置代理

ws_api = wechatsogou.WechatSogouAPI(proxies={
    "http": "127.0.0.1:8888",
    "https": '127.0.0.1:8888'
})

### 设置超时

ws_api = wechatsogou.WechatSogouAPI(timeout=0.1)

import wechatsogou

ws_api = wechatsogou.WechatSogouAPI()
ws_api.get_gzh_info('中美贸易战')

# 获取公众号文章信息
import os
import pickle
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import requests
import wechatsogou

# 发件人地址
from_address = 'cgzhang6436@163.com'
# 发件人邮箱密码
password = 'family404smtp'
# 邮箱服务器
smtp_server = 'smtp.163.com'

fail_count = 0
fail_list = []
sent_list = []
# 添加一个文件，将已经发送成功的文章标题序列化到文件，防止多次运行导致重复发送邮件
file_path = 'C:\\Users\\Franc\\Desktop\\Dir\# AutoMailAddress\\Path\\file.txt'

# 一些敏感词，简单过滤一下
sensitive_words = ['鄙视链', '中奖名单', '成功说一口流利英语', '婚姻', '恋爱']


ws_api = wechatsogou.WechatSogouAPI()

# 获取公众号文章信息
def get_article(gzh):
    articles = ws_api.get_gzh_article_by_history(gzh)
    print(len(articles['article']))
    return articles['article']

# 设置下编码
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发送邮件
def send_mail(to_address, subject, msg_html):

    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_address, password)
    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg = MIMEText(msg_html, 'html', 'utf-8')
    msg['From'] = _format_addr('张春光 <%s>' % from_address)
    msg['To'] = _format_addr(' Dear ')
    msg['Subject'] = Header(subject, 'utf-8').encode()
    try:
        server.sendmail(from_address, to_address, msg.as_string())
    except:
        global fail_count
        fail_count += 1
        fail_list.append(subject)


if '__main__' == __name__:
    # 定义一个公众号列表
    gzh_list = ['全栈布道士', '编程人生', 'importNew', 'Python开发者', '非著名程序员',
                'Python之美', '机器学习研究会', '程序员大咖', '51CTO', '纯洁的微笑']

    # 指定邮箱列表，这里有个建议，请邮件列表中将发件人添加到白名单，降低发送的失败率
    mail_list = ['cgzhang6436@163.com', '1559844145@qq.com', 'cgzhang6436@gmail.com',]
    for gzh in gzh_list:
        # 查找公众号之前，先从文件中反序列化出已经成功发送的文章列表
        if os.path.exists(file_path):
            f = open(file_path, 'rb')
            sent_list = pickle.load(f)
            f.close()
        articles = get_article(gzh)
        for article in articles:
            print(article['title'],'\n\t' ,article['content_url'])
            fileid = str(article['send_id']) + '_' + str(article['fileid'])
            # 如果新文章不在文章列表中，则发送
            if fileid not in sent_list:
                response_text = requests.get(article['content_url']).text
                send_mail(mail_list, article['title'], response_text)
                sent_list.append(fileid)
        print('发布数量', len(articles), '失败数量', fail_count)
        print('=' * 40)
        for subject in fail_list:
            print(subject)
        # 单个公众号文章发送完毕后，将新的已发送文章列表序列化，防止出现中途退出，造成重复发送
        f = open(file_path, 'wb')
        pickle.dump(sent_list, f)
        f.close()