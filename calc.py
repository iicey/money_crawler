import time

import pymongo
import configparser

config = configparser.ConfigParser()

config.read('config.ini', encoding='utf-8')
host = config.get('localhost_mongodb', 'host')
port = int(config.get('localhost_mongodb', 'port'))

client = pymongo.MongoClient(host=host, port=port)
db = client.otc
now_time = int(time.time())
before_time = now_time - 86400
print(db.huobi_btc_buy.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}}))
client.close()
