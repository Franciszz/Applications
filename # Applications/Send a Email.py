import zmail, os
# ================================================================================================
# 请输入: 邮件标题、内容以及附件
# ================================================================================================

# 邮件标题
mail_title = 'Paper to Print.'
# 邮件正文
mail_text =  'This is hw2so coding part \n \n \n \n —————— \n 张春光 \n 厦门大学经济学院 \n cgzhang6436@163.com '
# 邮件附件
file_dir = 'C:\\Users\\Franc\\Desktop\\Dir\# AutoMailAddress\\Send'
mail_attach = []
def attachs(dir= file_dir):
    fname = os.listdir(dir)
    for name in fname:
        file = os.path.join(dir, name)
        mail_attach.append(file)
    return mail_attach
# ================================================================================================
# 请输入: 收件人和发件人
# ================================================================================================
account = {'cgzhang6436@163.com':'family404smtp',
           '1559844145@qq.com':'zwgrsxqmcknfgcjc'}
# 收件人
mail_sender = 'cgzhang6436@163.com'
# 发件人
mail_receivers = ['cgzhang6436@163.com', 'cgzhang6436@foxmail.com']
def send_mail(sender = mail_sender, receivers= mail_receivers):
    mail_attach = attachs()
    mail_content = {
        'subject': mail_title,
        'content': mail_text,
        'attachments': mail_attach}
    server = zmail.server(sender, account[sender])
    try:
        server.send_mail(receivers, mail_content)
        print('Email has been sent successfully, Mr.Zhang')
    except BaseException as e:
        print('Mail Failed Sent, Sorry. Error! ')
# ================================================================================================
# 发送邮件
# ================================================================================================
if __name__ == '__main__':
    send_mail()



