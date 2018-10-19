from splinter.browser import Browser
import time

speech = Browser(driver_name='chrome')
url = 'http://account.soe.xmu.edu.cn/Account?returnUrl=%2FHome&err=noauthentication'
speech_url = url
speech.visit(url)
#登录页
def login(speech):
    speech.find_by_text(u'使用厦门大学统一账号登录').click()
    speech.fill('UserName', '15420171151976')
    speech.fill('Password', 'family404xmu')
    speech.find_by_id('LoginButton').click()
    speech.find_by_text(u'两院讲座预约系统').click()
    time.sleep(3)
    return speech
#讲座
def loop(speech):
    try: if


