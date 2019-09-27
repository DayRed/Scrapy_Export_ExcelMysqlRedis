# -*-coding:GBK -*-
from urllib import response
import scrapy
from xxoo.items import ForprogrammerItem
class GoGo(scrapy.Spider):
    name = "gogogo"

    start_urls = ['https://www.proginn.com/cat/']

    def parse(self, response):
        # 遍历当前页 所有人的主页链接地址
        cxy = response.xpath("//div[@class='user-avatar ui tiny image']//@href").extract()
        for i in cxy:
            yield scrapy.Request(url=i, callback=self.zh, dont_filter=True)  # 爬取到的页面如何处理？提交给zh方法处理

    def zh(self, response):
        item = ForprogrammerItem()

        introduction = response.xpath("string(//div[@class='introduction'])").extract()[0]                              # 个人简介
        item['introduction'] = introduction.replace('\n', '').replace(' ','').replace(',','-')

        workAndStudyExperience = response.xpath("//ul[@class='J_Works']//text()").extract()                             #工作经历+教育经历
        if len(workAndStudyExperience)>0:
            item['workAndStudyExperience'] = ','.join(workAndStudyExperience).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['workAndStudyExperience'] = '无'

        skill = response.xpath("//div[@class='skill-list']//text()").extract()                                          #技能
        if len(skill)>0:
            item['skill'] = ','.join(skill).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['skill'] = '无'

        moneyAndWork = response.xpath("//div[@class='hire-info']//p//text()").extract()                                 # 获取薪资及工作特点
        if len(moneyAndWork)>0:
            item['moneyAndWork'] = ','.join(moneyAndWork).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['moneyAndWork'] = '无'

        zuopin = response.xpath(                                                                                        #作品
            "//div[@class='work-list']//ul//li//a[@class='media']//div[@class='info']//p//text()").extract()
        item['zuopin'] = ','.join(zuopin).replace(' ', '')

        # ------------------ 以下内容是对照数据库 二次再加的-------------------------------------
        #城市
        user_city = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_city)==3:
            item['user_city'] = user_city[1]
        elif len(user_city)==2:
            item['user_city'] = '-'

        #现在公司名称
        user_nowcompany = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowcompany)==3:
            item['user_nowcompany'] = user_nowcompany[2].split()[0]
        elif len(user_city)==2:
            item['user_nowcompany'] = user_nowcompany[1].split()[0]

        #现在公司职称
        user_nowoccupation = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowoccupation)==3:
            item['user_nowoccupation'] = user_nowoccupation[2].split()[1]
        elif len(user_city)==2:
            item['user_nowoccupation'] = user_nowoccupation[1].split()[1]

        #个人介绍
        user_introduction = response.xpath("string(//div[@class='overflowhidden editor-style content'])").extract()[0]
        item['user_introduction'] = user_introduction.replace('\n', '').replace(' ', '').replace(',', '-')

        #期望日薪
        user_expectsalary = response.xpath("string(//div[@class='hire-info']//p[@class='work-price'])").extract()[0]
        item['user_expectsalary'] = user_expectsalary

        #毕业院校
        user_school = response.xpath("//div[@class='panel proginn-work-history'][last()]//p[@class='title']//span[2]//text()").extract()[0]
        item['user_school'] = user_school

        #评论数
        user_comment_number = response.xpath("//div[@id='proginn_wo_omment']//div[@class='content']//div[@class='content']//a").extract()
        item['user_comment_number'] = len(user_comment_number)

        #爬取源链接
        source_link = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        item['source_link'] = source_link

        #非假期每日工作时长
        #user_noworktime = response.xpath("//div[@class='hire-info']//p[last()]//text()").extract()[0]
        #item['user_noworktime'] = user_noworktime

        #github
        #github = response.xpath("//div[@class='social-list']//a/@href").extract()[0]
        #item['github'] = github

        #能力描述
        user_ability_describe = response.xpath("//div[@class='verify']//text()").extract()
        item['user_ability_describe'] = ','.join(user_ability_describe).lstrip().replace(',',' ').lstrip()

        #姓名
        user_name = response.xpath("//a[@class='header']//text()").extract()[0]
        item['user_name'] = user_name

        #头像
        user_picturehead = response.xpath("//div[@class='four wide column side-profile']//a//img//@src").extract()[0]
        item['user_picturehead'] = user_picturehead

        #用户详情的id
        details_id = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        item['details_id'] = details_id[27:]

        yield item