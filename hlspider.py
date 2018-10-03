# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from taonan.items import TaonanItem


class HlspiderSpider(RedisCrawlSpider):
    name = 'hlspider'
    # allowed_domains = ['taonanw.com']
    # start_urls = ['http://www.taonanw.com/?page=search_result_v2&search_type=search_quick&page_key=93e0a62a085397e93da5ed4bb727e0be&match_gender=1&match_r_state_id=6922&match_age_min=18&match_age_max=25&is_cut_img=1']
    redis_key = "hlspider:start_urls"
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(HlspiderSpider, self).__init__(*args, **kwargs)
    page_links = LinkExtractor(allow = (r"http://www.taonanw.com/page/search_result_v2/p/\d+/search_type/search_quick/page_key/93e0a62a085397e93da5ed4bb727e0be/match_gender/1/match_r_state_id/6922/match_age_min/18/match_age_max/25/is_cut_img/1/items_file/search_result_v2/total/813/n/20/list_style/2"))
    profile_links = LinkExtractor(allow = (r"www.taonanw.com/u_\d+"))



    rules = (
        Rule(page_links),
        Rule(profile_links,callback="parse_item" ),
    )


    def parse_item(self, response):
        item = TaonanItem()
        item["name"] = response.xpath("//h1/text()").extract()
        item["job"] =  response.xpath('//span[@id="profile_occupation"]/a/text()').extract()
        item["education"] =  response.xpath('//span[@id="profile_education"]/text()').extract()
        item["income"] =  response.xpath('//span[@id="profile_income"]/text()').extract()
        item["age"] =  response.xpath('//span[@id="profile_age"]/text()').extract()
        item["photo"] =  response.xpath('//div[@class="profile-user-img-box"]//img/@src').extract()
        item["sologan"] =  response.xpath('//div[@class="profile-about profile-box"]/span/text()').extract()

        yield item
