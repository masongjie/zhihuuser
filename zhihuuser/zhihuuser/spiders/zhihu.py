# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
    start_user = "ggg-ah"



    followees_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    followees_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"

    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"

    def start_requests(self):
        #初始个人请求
        yield scrapy.Request(url=self.user_url.format(user=self.start_user,include=self.user_query),callback=self.user_parse)
        #初始关注着请求
        yield scrapy.Request(url=self.followees_url.format(user=self.start_user,include=self.followees_query,offset=0,limit=20),callback=self.followees_parse)
        #初始化被关注着
        yield scrapy.Request(url=self.followers_url.format(user=self.start_user,include= self.followers_query,offset=0,limit=20),callback=self.followers_query)

    def user_parse(self,response):
        results = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field] =results.get(field)
        yield item

        yield scrapy.Request(self.user_url.format(user=results.get('url_token'),include=self.user_query),callback=self.user_parse)
        yield scrapy.Request(self.followers_url.format(user=results.get('url_token'),include=self.followers_query,offset=0,limit=20),callback=self.followers_parse)

    def followees_parse(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include =self.user_query),
                                     callback=self.user_parse)
            if 'paging' in results.keys() and results.get('paging').get('is_end')== False:
                yield scrapy.Request(results.get('paging').get('next'),callback=self.followees_parse)


    def followers_parse(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include =self.user_query),
                                     callback=self.user_parse)
            if 'paging' in results.keys() and results.get('paging').get('is_end')== False:
                yield scrapy.Request(results.get('paging').get('next'),callback=self.followers_parse)


    def parse(self, response):
        print(response.text)



