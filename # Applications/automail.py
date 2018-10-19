# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:43:51 2018

@author: Franc
"""
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL, SMTPException

###################################################
################ QQ邮箱 ###########################
###################################################
##qq邮箱smtp服务器
host_server = 'smtp.qq.com'
#sender_qq为发件人的qq号码
sender_qq = '1559844145'
#pwd为qq邮箱的授权码
pwd = 'zwgrsxqmcknfgcjc'
#发件人的邮箱
sender_qq_mail = '1559844145@qq.com'
#收件人邮箱
receiver = 'cgzhang6436@163.com'
#邮件的正文内容
mail_content = 'Python Test'
#邮件标题
mail_title = 'Evans的邮件'
#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)
msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()
###################################################
################163邮箱 ###########################
###################################################
from email.mime.text import MIMEText
from email.header import Header
import smtplib
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "cgzhang6436"       #用户名
mail_pwd = "family404smtp"
mail_sender = 'cgzhang6436@163.com'    # 发件人邮箱(最好写全, 不然会失败)
mail_receivers = ['1559844145@qq.com','cgzhang6436@gmail.com']
mail_content = 'AutoMailPython'
mail_title = 'Test'
def sendEmail(user=mail_user,password=mail_pwd,
              sender=mail_sender,receiver=mail_receivers,
              content=mail_content,title=mail_title,
              host=mail_host):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receiver)
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(host, 465)
        smtpObj.login(user,password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("mail has been send successfully.")
    except SMTPException as e:
        print(e)
if __name__ == '__main__':
    sendEmail()
    # receiver = '***'
    # send_email2(mail_host, mail_user, mail_pass, receiver, title, content)

def send_email2(SMTP_host,from_account,from_passwd,
                to_account,subject,content):
    email_client =  smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())
    email_client.quit()
###################################################
################Zmail##############################
###################################################
import zmail
# 邮件内容
mail_content  = {
    'subject' : 'Solutions for Homework3',
    'content' : 'This is the solution for homework3 \n \n \n \n —————— \n 张春光 \n 厦门大学经济学院 \n cgzhang6436@163.com ',
    'attachments' : 'C:/Users/Franc/Desktop/Cur/# Course/M.S.&TA/Solutions/solution3_update/hw3so.pdf'
}
#登陆服务器
server = zmail.server('cgzhang6436@163.com', 'family404smtp')
#发送邮件
server.send_mail(['cgzhang6436@foxmail.com','cgzhang6436@gmail.com'], mail_content)

###################################################
################Zmail_HTML#########################
###################################################
mail = {
    'subject': 'Success!',  # Anything you want.
    'content_html': zmail.get_html('html_path'), # Absolute path will be better.
    'attachments': '/Users/zyh/Documents/example.zip',  # Absolute path will be better.
}
server.send_mail('yourfriend@example.com',mail)
###################################################
################查收邮件###########################
###################################################
import zmail
server = zmail.server('cgzhang6436@163.com', 'family404smtp')
mail = server.get_latest()
mail['subject']#邮件标题
mail = server.get_mail(3)#第二封邮件
mail = server.get_mails(subject='GitHub',after='2018-1-1',sender='github')# 条件搜索邮件
# 解析邮件信息
mail_info = server.get_info()
mailbox_info = server.stat()
# 展示邮件
import zmail
server = zmail.server('cgzhang6436@163.com', 'family404smtp')
mail = server.get_latest()
zmail.show(mail)
# 获得附件
zmail.get_attachment(mail)
# 保存邮件
import zmail
server = zmail.server('cgzhang6436@163.com', 'family404smtp')
mail = server.get_latest()
zmail.save_eml(mail)
zmail.save_eml(mail,name='hello.eml',path='/usr/home')
# 读取磁盘上的邮件
import zmail
mail_as_raw = zmail.read_eml('/usr/home/hello.eml') # Abspath will be better
# 解析成zmail格式邮件
mail = zmail.decode(mail_as_raw)
