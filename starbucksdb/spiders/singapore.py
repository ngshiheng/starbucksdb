import json

import scrapy

from starbucksdb.utils.parsers import parse_store_data


class SingaporeSpider(scrapy.Spider):
    name = "singapore"
    allowed_domains = ["static.sbux.mobi"]
    endpoint = "https://static.sbux.mobi"

    def start_requests(self):
        stores_url = f"{self.endpoint}/json/mop/stores.json"
        yield scrapy.Request(url=stores_url, callback=self.parse_stores)

    def parse_stores(self, response):
        stores_data = json.loads(response.body)["Data"]

        for store in stores_data:
            store_item = parse_store_data(store)
            yield store_item
