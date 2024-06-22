import json

import scrapy

from starbucksdb.utils.parsers import parse_menu_data, parse_store_data


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

            branch_code = store["BranchCode"]
            menu_url = f"{self.endpoint}/json/mop/menu/{branch_code}.json"
            yield scrapy.Request(
                url=menu_url,
                callback=self.parse_menu,
                meta={"branch_code": branch_code},
            )

    def parse_menu(self, response):
        menu_data = json.loads(response.body)["Data"][0]
        branch_code = response.meta["branch_code"]

        assert branch_code == menu_data["BranchCode"], "Branch code mismatch"

        menu_item = parse_menu_data(menu_data)

        yield menu_item
