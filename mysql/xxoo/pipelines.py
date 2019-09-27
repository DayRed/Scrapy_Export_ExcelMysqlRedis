# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter


from twisted.enterprise import adbapi
from pymysql import cursors
import pymysql
class ForprogrammerPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'forprogrammers',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['user_city'],item['user_nowcompany'],item['user_nowoccupation'],item['user_introduction']
                                       ,item['user_expectsalary'],item['user_school'],item['user_comment_number'],item['source_link']
                                       ,item['user_ability_describe'],item['user_name'],item['user_picturehead']
                                       ,item['details_id']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into zc_user_details(user_city,user_nowcompany,user_nowoccupation,user_introduction,
                user_expectsalary,user_school,user_comment_number,source_link,user_ability_describe,
                user_name,user_picturehead,details_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql















































    '''
    def __init__(self):
        self.row = 0
        print("***********************生成excel文件***************************")
        self.wb = xlsxwriter.Workbook("程序员客栈.xlsx")
        self.ws = self.wb.add_worksheet()
        self.title = [ '个人简介', '工作教育经历','技能','薪资及工作特点','作品',                                            #设置表头
        #------------------ 以下内容是对照数据库 二次再加的-------------------------------------
                      '城市','现在公司名称','现在公司职称','个人介绍',
                      '期望日薪','毕业院校','评论数',
                      '爬取源链接','能力描述','姓名','头像',
                      '用户详情的id'
                      ]
        self.ws.write_row(self.row, 0, self.title)

    def process_item(self, item, spider):
        self.row += 1
        line = [item['introduction'],item['workAndStudyExperience'],item['skill'],item['moneyAndWork'],item['zuopin']
        #------------------ 以下内容是对照数据库 二次再加的-------------------------------------
                ,item['user_city'],item['user_nowcompany'],item['user_nowoccupation'],item['user_introduction']         #把数据中每一项整理出来
                ,item['user_expectsalary'],item['user_school'],item['user_comment_number']
                ,item['source_link'],item['user_ability_describe'],item['user_name'],item['user_picturehead']
                ,item['details_id']
                ]
        self.ws.write_row(self.row, 0, line)
        return item

    def close_spider(self, spider):
        self.wb.close()

    '''