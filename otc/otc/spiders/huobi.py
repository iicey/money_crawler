# -*- coding: utf-8 -*-
import json
import time
from itertools import product

import scrapy
import pymongo
import configparser

config = configparser.ConfigParser()

config.read('config.ini', encoding='utf-8')
host = config.get('localhost_mongodb', 'host')
port = int(config.get('localhost_mongodb', 'port'))

client = pymongo.MongoClient(host=host, port=port)
db = client.otc


class HuoBiSpider(scrapy.Spider):
    name = 'huobi'
    allowed_domains = ['otc-api-bj.eiijo.cn']

    def start_requests(self):
        for x, y in product(['1', '2', '3', '5'], ['sell', 'buy']):
            yield scrapy.FormRequest(url='https://otc-api-bj.eiijo.cn/v1/data/trade-market',
                                     formdata={'coinId': x, 'currency': '1', 'tradeType': y, 'currPage': '1',
                                               'payMethod': '0', 'country': '37', 'blockType': 'general',
                                               'online': '1'}, method='GET')

    def parse(self, response):
        request_url = response.url
        response = json.loads(response.text)
        data_list = response.get("data")
        first_price = data_list[0].get("price")
        dt = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
        timestamp = str(int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M"))))
        item = dict()
        item['_id'] = timestamp
        item['price'] = first_price
        if 'coinId=1' in request_url and 'buy' in request_url:
            db.huobi_btc_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_btc_buy: {item}")
        if 'coinId=2' in request_url and 'buy' in request_url:
            db.huobi_usdt_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_usdt_buy: {item}")
        if 'coinId=3' in request_url and 'buy' in request_url:
            db.huobi_eth_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_eth_buy: {item}")
        if 'coinId=4' in request_url and 'buy' in request_url:
            db.huobi_ht_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_ht_buy: {item}")
        if 'coinId=5' in request_url and 'buy' in request_url:
            db.huobi_eos_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_eos_buy: {item}")
        if 'coinId=6' in request_url and 'buy' in request_url:
            db.huobi_husd_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_husd_buy: {item}")
        if 'coinId=7' in request_url and 'buy' in request_url:
            db.huobi_xrp_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_xrp_buy: {item}")
        if 'coinId=8' in request_url and 'buy' in request_url:
            db.huobi_ltc_buy.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_ltc_buy: {item}")

        if 'coinId=1' in request_url and 'sell' in request_url:
            db.huobi_btc_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_btc_sell: {item}")
        if 'coinId=2' in request_url and 'sell' in request_url:
            db.huobi_usdt_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_usdt_sell: {item}")
        if 'coinId=3' in request_url and 'sell' in request_url:
            db.huobi_eth_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_eth_sell: {item}")
        if 'coinId=4' in request_url and 'sell' in request_url:
            db.huobi_ht_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_ht_sell: {item}")
        if 'coinId=5' in request_url and 'sell' in request_url:
            db.huobi_eos_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_eos_sell: {item}")
        if 'coinId=6' in request_url and 'sell' in request_url:
            db.huobi_husd_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_husd_sell: {item}")
        if 'coinId=7' in request_url and 'sell' in request_url:
            db.huobi_xrp_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_xrp_sell: {item}")
        if 'coinId=8' in request_url and 'sell' in request_url:
            db.huobi_ltc_sell.update_one({"_id": timestamp}, {"$set": item}, upsert=True)
            self.logger.info(f"huobi_ltc_sell: {item}")


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl huobi".split())
