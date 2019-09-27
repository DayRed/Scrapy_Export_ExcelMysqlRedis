# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForprogrammerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
    introduction = scrapy.Field()
    workAndStudyExperience = scrapy.Field()
    skill = scrapy.Field()
    works = scrapy.Field()
    moneyAndWork = scrapy.Field()
    zuopin = scrapy.Field()# 作品
    '''


    user_city = scrapy.Field()                          #城市
    user_nowcompany = scrapy.Field()                    #现在公司名称
    user_nowoccupation = scrapy.Field()                 #现在公司职称
    user_introduction = scrapy.Field()                  #个人介绍
    user_expectsalary = scrapy.Field()                  #期望日薪
    user_school = scrapy.Field()                        #毕业院校
    user_comment_number = scrapy.Field()                #评论数
    source_link = scrapy.Field()                        #爬取源链接
    #user_noworktime = scrapy.Field()                    #非假期每日工作时长
    #github = scrapy.Field()                             #github地址
    user_ability_describe = scrapy.Field()              #能力描述
    user_name = scrapy.Field()                          #姓名
    user_picturehead = scrapy.Field()                   #头像
    source_id = scrapy.Field()                          #源数据id
    user_consultingsources = scrapy.Field()             #信息来源

