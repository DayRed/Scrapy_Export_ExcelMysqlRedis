# -*-coding:GBK -*-
from urllib import response
import scrapy
from xxoo.items import ForprogrammerItem
class GoGo(scrapy.Spider):
    name = "gogogo"

    start_urls = ['https://www.proginn.com/cat/']

    def parse(self, response):
        # ������ǰҳ �����˵���ҳ���ӵ�ַ
        cxy = response.xpath("//div[@class='user-avatar ui tiny image']//@href").extract()
        for i in cxy:
            yield scrapy.Request(url=i, callback=self.zh, dont_filter=True)  # ��ȡ����ҳ����δ����ύ��zh��������

    def zh(self, response):
        item = ForprogrammerItem()

        introduction = response.xpath("string(//div[@class='introduction'])").extract()[0]                              # ���˼��
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

        moneyAndWork = response.xpath("//div[@class='hire-info']//p//text()").extract()                                 # ��ȡн�ʼ������ص�
        if len(moneyAndWork)>0:
            item['moneyAndWork'] = ','.join(moneyAndWork).replace('\n', '').replace(' ','').replace(',','-')
        else:
            item['moneyAndWork'] = '��'

        zuopin = response.xpath(                                                                                        #��Ʒ
            "//div[@class='work-list']//ul//li//a[@class='media']//div[@class='info']//p//text()").extract()
        item['zuopin'] = ','.join(zuopin).replace(' ', '')

        # ------------------ ���������Ƕ������ݿ� �����ټӵ�-------------------------------------
        #����
        user_city = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_city)==3:
            item['user_city'] = user_city[1]
        elif len(user_city)==2:
            item['user_city'] = '-'

        #���ڹ�˾����
        user_nowcompany = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowcompany)==3:
            item['user_nowcompany'] = user_nowcompany[2].split()[0]
        elif len(user_city)==2:
            item['user_nowcompany'] = user_nowcompany[1].split()[0]

        #���ڹ�˾ְ��
        user_nowoccupation = response.xpath("//div[@class='introduction']//text()").extract()
        if len(user_nowoccupation)==3:
            item['user_nowoccupation'] = user_nowoccupation[2].split()[1]
        elif len(user_city)==2:
            item['user_nowoccupation'] = user_nowoccupation[1].split()[1]

        #���˽���
        user_introduction = response.xpath("string(//div[@class='overflowhidden editor-style content'])").extract()[0]
        item['user_introduction'] = user_introduction.replace('\n', '').replace(' ', '').replace(',', '-')

        #������н
        user_expectsalary = response.xpath("string(//div[@class='hire-info']//p[@class='work-price'])").extract()[0]
        item['user_expectsalary'] = user_expectsalary

        #��ҵԺУ
        user_school = response.xpath("//div[@class='panel proginn-work-history'][last()]//p[@class='title']//span[2]//text()").extract()[0]
        item['user_school'] = user_school

        #������
        user_comment_number = response.xpath("//div[@id='proginn_wo_omment']//div[@class='content']//div[@class='content']//a").extract()
        item['user_comment_number'] = len(user_comment_number)

        #��ȡԴ����
        source_link = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        item['source_link'] = source_link

        #�Ǽ���ÿ�չ���ʱ��
        #user_noworktime = response.xpath("//div[@class='hire-info']//p[last()]//text()").extract()[0]
        #item['user_noworktime'] = user_noworktime

        #github
        #github = response.xpath("//div[@class='social-list']//a/@href").extract()[0]
        #item['github'] = github

        #��������
        user_ability_describe = response.xpath("//div[@class='verify']//text()").extract()
        item['user_ability_describe'] = ','.join(user_ability_describe).lstrip().replace(',',' ').lstrip()

        #����
        user_name = response.xpath("//a[@class='header']//text()").extract()[0]
        item['user_name'] = user_name

        #ͷ��
        user_picturehead = response.xpath("//div[@class='four wide column side-profile']//a//img//@src").extract()[0]
        item['user_picturehead'] = user_picturehead

        #�û������id
        details_id = response.xpath("//head//link[@rel='canonical']//@href").extract()[0]
        item['details_id'] = details_id[27:]

        yield item