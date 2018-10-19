# ================================================================================================
# 基础知识
# ================================================================================================
from splinter.browser import Browser
ticket = Browser(driver_name = 'chrome')
ticket.visit('http://www.zhihu.com/')
## xx.fill("wd", "dataman")即可在搜索栏搜索dataman
## button = xx.find_by_value(u"提问")
button = ticket.find_by_id(u"zu-top-add-questionSBSBSBSBSBSBSB")

# ================================================================================================
# 12306抢票
# ================================================================================================
from splinter.browser import Browser
client = Browser(driver_name= 'chrome')
url = 'https://kyfw.12306.cn/otn/leftTicket/init'
client.visit(url)
client.find_by_text(u'登录').click()
client.fill('loginUserDTO.user_name','1559844145@qq.com')
client.fill("userDTO.password","family40440412306")
#填写出发点目的地
client.cookies.add({"_jc_save_fromStation":"%u4E0A%u6D77%2CSHH"})
client.cookies.add({"_jc_save_fromDate":"2016-01-20"})
client.cookies.add({u'_jc_save_toStation':'%u6C38%u5DDE%2CAOQ'})
#加载查询
client.reload()
client.find_by_text(u"查询").click()
#预定
client.find_by_text(u"预订")[1].click()
#选择乘客
client.find_by_text(u"数据分析侠")[1].click()

#-*- coding:utf-8 -*-
#京东抢手机脚本
from splinter.browser import Browser
import time

#登录页
def login(b):  #登录京东
    b.click_link_by_text("你好，请登录")
    time.sleep(3)
    b.fill("loginname","account*****")  #填写账户密码
    b.fill("nloginpwd","passport*****")
    b.find_by_id("loginsubmit").click()
    time.sleep(3)
    return b

#订单页
def loop(b):  #循环点击
    try:
        if b.title=="订单结算页 -京东商城":
            b.find_by_text("保存收货人信息").click()
            b.find_by_text("保存支付及配送方式").click()
            b.find_by_id("order-submit").click()
            return b
        else:  #多次抢购操作后，有可能会被转到京东首页，所以要再打开手机主页
            b.visit("http://item.jd.com/2707976.html")
            b.find_by_id("choose-btn-qiang").click()
            time.sleep(10)
            loop(b)  #递归操作
    except Exception as e: #异常情况处理，以免中断程序
        b.reload()  #重新刷新当前页面，此页面为订单提交页
        time.sleep(2)
        loop(b)  #重新调用自己


b=Browser(driver_name="chrome") #打开浏览器
b.visit("http://item.jd.com/2707976.html")
login(b)
b.find_by_id("choose-btn-qiang").click() #找到抢购按钮，点击
time.sleep(10)  #等待10sec
while True:
    loop(b)
    if b.is_element_present_by_id("tryBtn"): #订单提交后显示“再次抢购”的话
        b.find_by_id("tryBtn").click()  #点击再次抢购，进入读秒5，跳转订单页
        time.sleep(6.5)
    elif b.title=="订单结算页 -京东商城": #如果还在订单结算页
        b.find_by_id("order-submit").click()
    else:
        print('恭喜你，抢购成功')
        break
