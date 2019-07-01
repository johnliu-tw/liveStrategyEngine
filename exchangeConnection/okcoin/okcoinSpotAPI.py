#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 用于访问OKCOIN 现货REST API
from exchangeConnection.okcoin.httpMD5Util import buildMySign, httpGet, httpPost
from utils.helper import *
import calendar;
import time;


class OKCoinSpot:
    def __init__(self, url, apikey, secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    # 获取OKCOIN现货行情信息
    def ticker(self, symbol=''):
        TICKER_RESOURCE = "/v1/cash/public/symbols"
        params = ''
        
        return httpGet(self.__url, TICKER_RESOURCE, params)

    # 获取OKCOIN现货市场深度信息
    def depth(self, symbol='', size=5):
        DEPTH_RESOURCE = "/api/v1/depth"
        params = {}
        params['symbol']=symbol
        params['size']=size

        depth_data = httpGet(self.__url, DEPTH_RESOURCE, params)
        if depth_data == "Timeout":
            time.sleep(1)
            depth_data = httpGet(self.__url, DEPTH_RESOURCE, params)
            return depth_data
        else:
            return depth_data

    # 获取OKCOIN现货历史交易信息
    def trades(self, symbol=''):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return httpGet(self.__url, TRADES_RESOURCE, params)

    # 获取用户现货账户信息
    def userInfo(self):
        USERINFO_RESOURCE = "/v1/cash/accounts/balance"
        ts = int(time.time()*1000)
        params = {}
        params['apiAccessKey'] = self.__apikey
        params['apiTimeStamp'] = ts
        params['apiSign'] = buildMySign(params, self.__secretkey)

        user_info = httpGet(self.__url, USERINFO_RESOURCE, params)
        if user_info == "Timeout":
            ts = int(time.time()*1000)
            params['apiTimeStamp'] = ts
            params['apiSign'] = buildMySign(params, self.__secretkey)
            user_info = httpGet(self.__url, USERINFO_RESOURCE, params)
            time.sleep(1)
            return user_info
        else:
            return user_info

    # 现货交易
    def trade(self, contractId, tradeType,  price='', amount=''):
        TRADE_RESOURCE = "/v1/cash/trade/order"
        ts = int(time.time()*1000)
        params = {}
        url_params = {}
        url_params['apiAccessKey'] = self.__apikey
        url_params['apiTimeStamp'] = ts
        url_params['apiSign'] = buildMySign(url_params, self.__secretkey)
        params['side'] = tradeType
        params['orderType'] = 1
        params['contractId'] = contractId
        if price:
            params['price'] = int(price)
        if amount:
            params['quantity'] = amount
        
        print(params)

        return httpPost(self.__url, TRADE_RESOURCE, params, url_params=url_params)

    # 现货批量下单
    def batchTrade(self, symbol, tradeType, orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'type': tradeType,
            'orders_data': orders_data
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, BATCH_TRADE_RESOURCE, params)

    # 现货取消订单
    def cancelOrder(self, orderId, contractId):
        CANCEL_ORDER_RESOURCE = "/v1/cash/trade/order/cancel"
        ts = int(time.time()*1000)
        params = {}
        url_params = {}
        url_params['apiAccessKey'] = self.__apikey
        url_params['apiTimeStamp'] = ts
        url_params['orderId'] = orderId
        url_params['apiSign'] = buildMySign(url_params, self.__secretkey)
        params['contractId'] = contractId
        params['originalOrderId'] = orderId

        return httpPost(self.__url, CANCEL_ORDER_RESOURCE, params, url_params=url_params)

    # 现货订单信息查询
    def orderInfo(self, orderId):
        ORDER_INFO_RESOURCE = "/v1/cash/accounts/order/get"
        ts = int(time.time()*1000)
        url_params = {}
        url_params['apiAccessKey'] = self.__apikey
        url_params['apiTimeStamp'] = ts
        url_params['orderId'] = orderId
        url_params['apiSign'] = buildMySign(url_params, self.__secretkey)

        time.sleep(1)
        order_info = httpGet(self.__url, ORDER_INFO_RESOURCE, url_params)
        print(order_info['msg'])
        if order_info == "Timeout" or order_info['code'] == 2006 or order_info['msg'] == 'order no exist':
            ts = int(time.time()*1000)
            url_params['apiTimeStamp'] = ts
            url_params['apiSign'] = buildMySign(url_params, self.__secretkey)
            order_info = httpGet(self.__url, ORDER_INFO_RESOURCE, url_params)
            time.sleep(1)
            return order_info           
        else:
            return order_info

    # 现货批量订单信息查询
    def ordersInfo(self):
        ORDERS_INFO_RESOURCE = "/v1/cash/accounts/orders/get"
        ts = int(time.time()*1000)
        params = {}
        url_params = {}
        url_params['apiAccessKey'] = self.__apikey
        url_params['apiTimeStamp'] = ts
        url_params['apiSign'] = buildMySign(url_params, self.__secretkey)
        params = []
        
        return httpPost(self.__url, ORDERS_INFO_RESOURCE, params, url_params=url_params)

    # 现货获得历史订单信息
    def orderHistory(self, symbol, status, currentPage, pageLength):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': self.__apikey,
            'symbol': symbol,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, self.__secretkey)
        return httpPost(self.__url, ORDER_HISTORY_RESOURCE, params)

    # 获取最小订单数量
    # okcoin上比特币的交易数量是0.01的整数倍，莱特币交易数量是0.1的整数倍
    def getMinimumOrderQty(self, symbol):
        if symbol == COIN_TYPE_BTC_CNY:
            return 0.005
        else:
            return 0.0001
