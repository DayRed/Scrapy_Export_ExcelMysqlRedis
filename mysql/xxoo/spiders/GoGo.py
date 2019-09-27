# -*-coding:GBK -*-
from urllib import response
import scrapy
from xxoo.items import ForprogrammerItem
import os
class GoGo(scrapy.Spider):
    name = "gogogo"
    flag = True

    #start_urls = ['https://www.proginn.com/cat/']

    def start_requests(self):  # �ɴ˷���ͨ������������ȡҳ��
        # ������ȡ������
        purl = 'https://www.proginn.com/cat/'
        yield scrapy.Request(url=purl, callback=self.parse)


    def parse(self, response):
        self.flag = True
        # ������ǰҳ �����˵���ҳ���ӵ�ַ
        cxy = response.xpath("//div[@class='user-avatar ui tiny image']//@href").extract()

        for i in cxy:
            yield scrapy.Request(url=i, callback=self.zh)

        # ��ȡȫ��
        while self.flag != False:
            no = int(response.xpath("//div[@class='ui pagination menu']//a[@class='item active']//text()").extract()[0])
            if no > 9:
                if((no+10) % no ==0):
                    next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[2]
                else:
                    next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[int(no%10+2)]
            else:
                next_page = response.xpath("//div[@class='ui pagination menu']//a//@href").extract()[int(no)]  # �鿴��ľ�д�����һҳ����

            if next_page is not None:
                next_page = response.urljoin(next_page)    #������ڵĻ�������ʹ�ã�response.urljoin(next_page)�����·�����磺page/1ת��Ϊ����·����
                                                           #��ʵҲ���Ǽ�����վ�������磺http://lab.scrapyd.cn/page/1��
                self.flag = False
                yield scrapy.Request(next_page, callback=self.parse)

                # һ���ǣ����Ǽ�����ȡ�����ӣ�next_page������������һҳ���ӣ���ȻҲ����������ҳ��
                # ��һ���ǣ�����Ҫ�������ύ����һ��������ȡ��������parse������Ҳ���Ǳ�����

    def zh(self, response):
        item = ForprogrammerItem()

        '''
        introduction = response.xpath("string(//div[@class='introduction'])").extract()[0]                              #���˼��
        item['introduction'] = introduction.replace('\n', '').replace(' ','').replace(',','-')

        workAndStudyExperience = response.xpath("//ul[@class='J_Works']//text()").extract()                             #��������+��������
        if len(workAndStudyExperience)>0:
            item['workAndStudyExperience'] = ','.join(workAndStudyExperience).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['workAndStudyExperience'] = '��'

        skill = response.xpath("//div[@class='skill-list']//text()").extract()                                          #����
        if len(skill)>0:
            item['skill'] = ','.join(skill).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['skill'] = '��'

        moneyAndWork = response.xpath("//div[@class='hire-info']//p//text()").extract()                                 #��ȡн�ʼ������ص�
        if len(moneyAndWork)>0:
            item['moneyAndWork'] = ','.join(moneyAndWork).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['moneyAndWork'] = '��'

        zuopin = response.xpath(                                                                                        #��Ʒ
            "//div[@class='work-list']//ul//li//a[@class='media']//div[@class='info']//p//text()").extract()
        item['zuopin'] = ','.join(zuopin).replace(' ', '')
        '''
        # ------------------ ���������Ƕ������ݿ� �����ټӵ�-------------------------------------
        #����
        user_city = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_city)==3:
            user_city = user_city[1]
        elif len(user_city)==2:
            user_city = '-'

        #���ڹ�˾����
        user_nowcompany = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowcompany)==2:
            user_nowcompany = user_nowcompany[1].split()[0]
        elif len(user_nowcompany)==3:
            user_nowcompany = user_nowcompany[2].split()[0]

        #���ڹ�˾ְ��
        user_nowoccupation = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowoccupation)==2:
            user_nowoccupation = user_nowoccupation[1].split()[1]
        elif len(user_nowoccupation)==3:
            user_nowoccupation = user_nowoccupation[2].split()[1]

        #���˽���
        user_introduction = response.xpath("string(//div[@class='overflowhidden editor-style content'])").extract()[0]
        user_introduction = user_introduction.replace('\n', '').replace(' ', '').replace(',', '-')

        #������н
        user_expectsalary = response.xpath("string(//div[@class='hire-info']//p[@class='work-price'])").extract()[0]
        user_expectsalary = user_expectsalary

        #��ҵԺУ
        user_school = response.xpath("//div[@class='panel proginn-work-history'][last()]//p[@class='title']//span[2]//text()").extract()[0]
        user_school = user_school

        #������
        user_comment_number = response.xpath("//div[@id='proginn_wo_omment']//div[@class='content']//div[@class='content']//a").extract()
        user_comment_number = len(user_comment_number)

        #��ȡԴ����
        source_link = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        source_link = source_link

        #�Ǽ���ÿ�չ���ʱ��
        #user_noworktime = response.xpath("//div[@class='hire-info']//p[last()]//text()").extract()[0]
        #item['user_noworktime'] = user_noworktime

        #github
        #github = response.xpath("//div[@class='social-list']//a/@href").extract()[0]
        #item['github'] = github

        #��������
        user_ability_describe = response.xpath("//div[@class='verify']//text()").extract()
        user_ability_describe = ','.join(user_ability_describe).lstrip().replace(',',' ').lstrip()

        #����
        user_name = response.xpath("//a[@class='header']//text()").extract()[0]
        user_name = user_name

        #ͷ��
        user_picturehead = response.xpath("//div[@class='four wide column side-profile']//a//img//@src").extract()[0]
        user_picturehead = user_picturehead

        #�û������id
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