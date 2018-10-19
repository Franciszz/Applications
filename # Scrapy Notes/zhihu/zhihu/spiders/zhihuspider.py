# -*- coding: utf-8 -*-
import json
from zheye import zheye
import scrapy
import re
import time
from PIL import Image
from urllib import parse
from scrapy.loader import ItemLoader
from zhihu.items import ZhihuQuestionItem

class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }
    def parse(self,response):
        all_urls = response.css('a:attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https://www.zhihu.com/question/') else False, all_urls)
        for url in all_urls:
            # 把遍历过后的网址分成两组
            match_obj = re.match('(.*question/(\d+))(/|$)', url)
            if match_obj:
                request_url = match_obj.group(1)  # 请求url
                question_id = match_obj.group(2)  # 问题id
                yield scrapy.Request(request_url, headers=self.headers, meta={'question_id': question_id},
                                     callback=self.parse_question)
            else:
                # 如果不是正确的url,继续交给downloader执行
                yield scrapy.Request(url, headers=self.headers)

    def parse_question(self, response):
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        question_id = response.meta.get('question_id', '')
        item_loader.add_xpath('title', '//h1[@class="QuestionHeader-title"]/text()')
        item_loader.add_xpath('content', '//span[@class="RichText"]/text()')
        item_loader.add_value('zhihu_id', question_id)
        item_loader.add_value('url', response.url)
        item_loader.add_css('answer_num', '.List-headerText span::text')
        item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-value::text')
        item_loader.add_xpath('topics', '//div[@class="Popover"]/div/text()')
        article_item = item_loader.load_item()
        yield article_item

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/signup?next=%2F#signin', headers=self.headers, callback=self.login)]

    def login(self, response):
        """
        输入错误的账号和密码,可以判断出登录也需要提交xsrf
        获取_xsrf,  传递登录参数和验证码给下个函数
        """
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        if match_obj:
            xsrf = match_obj.group(1)
        if xsrf:
            post_data = {
                '_xsrf': xsrf,
                'phone_num': '1559844145@qq.com',
                'password': 'family404zh',
                'captcha': ''
            }
            t = str(int(time.time()))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(captcha_url, headers=self.headers, meta={'post_data': post_data},
                                 callback=self.login_after_captcha)

    def login_after_captcha_cn(selfs, response):
        with open('captcha.jpg', 'wb') as f:
            # 下载图片必须以二进制来传输
            f.write(response.body)
            f.close()

            # 导入者也库,知乎倒立文字验证码识别
        z = zheye()
        positions = z.Recognize('captcha.jpg')
        """ 
        者也传过来的坐标是倒序的,且数组的里面的值也是倒序的 
        最先识别的数组是图片的最后一个倒立文字,数组里面的数分别是y和x 
        """
        pos_arr = []
        # 有时候倒立一个字,有时候倒立两个字,根据传来的数组个数来决定走向
        if len(positions) == 2:
            # 如果第一个数组中的第二个数比第二个数组中的第二个大,也就是者也默认输出的
            # 举个例子[   [43,101],[52,194]   ]         # 排序前
            if positions[0][1] > positions[1][1]:
                # 把第二个数组放到最前面,再把里面的值互换位置,变成x轴和y轴
                pos_arr.append([positions[1][1], positions[1][0]])
                # 此时pos_arr列表是: [  [194,52]  ]

                # 第一个数组放到最后面,[0][1]放到前面,[0][0]放到后面
                pos_arr.append([positions[0][1], positions[0][0]])
                # 此时pos_arr列表是: [   [194,52],[101,43]   ]           # 排序后

            # 光是倒序,数值正常的
            else:
                # [   [101,43],[194,52]   ]         排序前
                pos_arr.append(positions[0][1], positions[0][0])
                pos_arr.append(positions[1][1], positions[1][0])
                # [   [43,101],[52,194]   ]         排序后
        # 只有一个数组的时候
        else:
            pos_arr.append([positions[0][1], positions[0][0]])

        post_data = response.meta.get('post_data', {})
        if len(positions) == 2:
            post_data['captcha'] = '{"img_size": [200, 44], "input_points": [[%.2f, %f], [%.2f, %f]]}' % \
                                   (pos_arr[0][0] / 2, pos_arr[0][1] / 2, pos_arr[1][0] / 2, pos_arr[1][1] / 2),
        else:

            post_data['captcha'] = '{"img_size": [200, 44], "input_points": [[%.2f, %f]}' % \
                                   (pos_arr[0][0] / 2, pos_arr[0][1] / 2)
        post_data['captcha_type'] = 'cn'
        post_url = 'https://www.zhihu.com/login/phone_num'

        # 最终提交用scrapy.FormRequest,参数也得是formdata
        return [scrapy.FormRequest(
            post_url,
            headers=selfs.headers,
            formdata=post_data,
            callback=selfs.check_login
        )]

    def login_after_captcha(self, response):
        # 一次session就是一次对话,长连接,第一次访问完之后下次在访问的时候直接带过去
        # 访问知乎的时候,不管有没有登录,都会在session的cookies里面放一些值,自带的
        # 其中就包括_xsrf和服务器设置的一些值
        # 拿requests去访问,实际上是单独的在建立一个session,这两次的session值是不一样的
        # 这两次的函数调用图片的就不匹配了
        with open('captcha.jpg', 'wb') as f:
            # 下载图片必须以二进制来传输
            f.write(response.body)
            f.close()
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass
        captcha = input('请输入验证码:\n')
        post_data = response.meta.get('post_data', {})
        post_data['captcha'] = captcha
        post_url = 'https://www.zhihu.com/login/phone_num'
        # 最终提交用scrapy.FormRequest,参数也得是formdata
        return [scrapy.FormRequest(
            post_url,
            headers=self.headers,
            formdata=post_data,
            callback=self.check_login
        )]

    def check_login(self, response):
        text_json = json.loads(response.text)
        print(text_json)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)


