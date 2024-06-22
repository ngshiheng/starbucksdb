import scrapy


class SingaporeSpider(scrapy.Spider):
    name = "singapore"
    allowed_domains = ["static.sbux.mobi"]
    start_urls = ["https://static.sbux.mobi"]

    def parse(self, response):
        pass
