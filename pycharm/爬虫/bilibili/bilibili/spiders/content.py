import scrapy


class ContentSpider(scrapy.Spider):
    name = 'content'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/v/popular/all/?spm_id_from=333.1007.0.0']

    def parse(self, response):
        print(response.text)


        li_list = response.xpath('/html/body/div[2]/div/div[2]/div/text()')
        print(li_list)
        # for li in li_list:
        #     title_ = li.xpath('./div[1]/div[2]/p/texy()').extract_first()
        #     author = li.xpath('./div[1]/div[2]/div/span/span/text()').extract_first()
        #     view = li.xpath('./div[1]/div[2]/div/p/span[1]/text()').extract_first()
        #     commit = li.xpath('./div[1]/div[2]/div/p/span[2]/text()').extract_first()
        #     print(f"tittle:{title},author:{author},view:{view},commit:{commit}")
        #     break