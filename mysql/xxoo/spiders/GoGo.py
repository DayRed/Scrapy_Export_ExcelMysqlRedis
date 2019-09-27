# -*-coding:GBK -*-
from urllib import response
import scrapy
from xxoo.items import ForprogrammerItem
import os
class GoGo(scrapy.Spider):
    name = "gogogo"
    flag = True

    #start_urls = ['https://www.proginn.com/cat/']

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        # 定义爬取的链接
        purl = 'https://www.proginn.com/cat/'
        yield scrapy.Request(url=purl, callback=self.parse)


    def parse(self, response):
        self.flag = True
        # 遍历当前页 所有人的主页链接地址
        cxy = response.xpath("//div[@class='user-avatar ui tiny image']//@href").extract()

        for i in cxy:
            yield scrapy.Request(url=i, callback=self.zh)

        # 爬取全网
        while self.flag != False:
            no = int(response.xpath("//div[@class='ui pagination menu']//a[@class='item active']//text()").extract()[0])
            if no > 9:
                if((no+10) % no ==0):
                    next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[2]
                else:
                    next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[int(no%10+2)]
            else:
                next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[int(no)]  # 查看有木有存在下一页链接

            if next_page is not None:
                next_page = response.urljoin(next_page)    #如果存在的话，我们使用：response.urljoin(next_page)把相对路径，如：page/1转换为绝对路径，
                                                           #其实也就是加上网站域名，如：http://lab.scrapyd.cn/page/1；
                self.flag = False
                yield scrapy.Request(next_page, callback=self.parse)

                # 一个是：我们继续爬取的链接（next_page），这里是下一页链接，当然也可以是内容页；
                # 另一个是：我们要把链接提交给哪一个函数爬取，这里是parse函数，也就是本函数

    def zh(self, response):
        item = ForprogrammerItem()

        '''
        introduction = response.xpath("string(//div[@class='introduction'])").extract()[0]                              #个人简介
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

        moneyAndWork = response.xpath("//div[@class='hire-info']//p//text()").extract()                                 #获取薪资及工作特点
        if len(moneyAndWork)>0:
            item['moneyAndWork'] = ','.join(moneyAndWork).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['moneyAndWork'] = '无'

        zuopin = response.xpath(                                                                                        #作品
            "//div[@class='work-list']//ul//li//a[@class='media']//div[@class='info']//p//text()").extract()
        item['zuopin'] = ','.join(zuopin).replace(' ', '')
        '''
        # ------------------ 以下内容是对照数据库 二次再加的-------------------------------------
        #城市
        user_city = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_city)==3:
            user_city = user_city[1]
        elif len(user_city)==2:
            user_city = '-'

        #现在公司名称
        user_nowcompany = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowcompany)==2:
            user_nowcompany = user_nowcompany[1].split()[0]
        elif len(user_nowcompany)==3:
            user_nowcompany = user_nowcompany[2].split()[0]

        #现在公司职称
        user_nowoccupation = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowoccupation)==2:
            user_nowoccupation = user_nowoccupation[1].split()[1]
        elif len(user_nowoccupation)==3:
            user_nowoccupation = user_nowoccupation[2].split()[1]

        #个人介绍
        user_introduction = response.xpath("string(//div[@class='overflowhidden editor-style content'])").extract()[0]
        user_introduction = user_introduction.replace('\n', '').replace(' ', '').replace(',', '-')

        #期望日薪
        user_expectsalary = response.xpath("string(//div[@class='hire-info']//p[@class='work-price'])").extract()[0]
        user_expectsalary = user_expectsalary

        #毕业院校
        user_school = response.xpath("//div[@class='panel proginn-work-history'][last()]//p[@class='title']//span[2]//text()").extract()[0]
        user_school = user_school

        #评论数
        user_comment_number = response.xpath("//div[@id='proginn_wo_omment']//div[@class='content']//div[@class='content']//a").extract()
        user_comment_number = len(user_comment_number)

        #爬取源链接
        source_link = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        source_link = source_link

        #非假期每日工作时长
        #user_noworktime = response.xpath("//div[@class='hire-info']//p[last()]//text()").extract()[0]
        #item['user_noworktime'] = user_noworktime

        #github
        #github = response.xpath("//div[@class='social-list']//a/@href").extract()[0]
        #item['github'] = github

        #能力描述
        user_ability_describe = response.xpath("//div[@class='verify']//text()").extract()
        user_ability_describe = ','.join(user_ability_describe).lstrip().replace(',',' ').lstrip()

        #姓名
        user_name = response.xpath("//a[@class='header']//text()").extract()[0]
        user_name = user_name

        #头像
        user_picturehead = response.xpath("//div[@class='four wide column side-profile']//a//img//@src").extract()[0]
        user_picturehead = user_picturehead

        #用户详情的id
        details_id = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        details_id = details_id[27:]

        item = ForprogrammerItem(
            user_city = user_city,
            user_nowcompany = user_nowcompany,
            user_nowoccupation= user_nowoccupation,
            user_introduction = user_introduction,
            user_expectsalary = user_expectsalary,
            user_school= user_school,
            user_comment_number = user_comment_number,
            source_link = source_link,
            user_ability_describe = user_ability_describe,
            user_name = user_name,
            user_picturehead = user_picturehead,

            details_id = details_id
        )

        yield item