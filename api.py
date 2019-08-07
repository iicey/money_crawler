# coding: utf-8
import time

import pymongo
import configparser

from flask import Flask, views, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/*')
config = configparser.ConfigParser()

config.read('config.ini', encoding='utf-8')
host = config.get('localhost_mongodb', 'host')
port = int(config.get('localhost_mongodb', 'port'))


@app.route('/')
def index():
    return render_template('index.html')


class OTCHuoBi(views.MethodView):

    def get(self):
        client = pymongo.MongoClient(host=host, port=port)
        db = client.otc
        now_time = int(time.time())
        before_time = now_time - 86400
        result = None
        coin, trade = request.args.get('coin'), request.args.get('trade')
        if coin == 'btc' and trade == 'sell':
            result = db.huobi_btc_sell.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'usdt' and trade == 'sell':
            result = db.huobi_usdt_sell.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'eth' and trade == 'sell':
            result = db.huobi_eth_sell.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'eos' and trade == 'sell':
            result = db.huobi_eos_sell.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})

        if coin == 'btc' and trade == 'buy':
            result = db.huobi_btc_buy.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'usdt' and trade == 'buy':
            result = db.huobi_usdt_buy.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'eth' and trade == 'buy':
            result = db.huobi_eth_buy.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        if coin == 'eos' and trade == 'buy':
            result = db.huobi_eos_buy.find({"_id": {"$gte": str(before_time), "$lte": str(now_time)}})
        client.close()
        return jsonify(list(result))


app.add_url_rule("/otc", view_func=OTCHuoBi.as_view(name="OTCHuoBi"), methods=['GET'])

if __name__ == '__main__':
    app.run("0.0.0.0", 6688, threaded=True)
    # app.run("0.0.0.0", 6688, threaded=True, processes=3)
