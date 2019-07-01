#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

import base64
import datetime
import hashlib
import hmac
import json
import time
import urllib
import urllib.parse
import urllib.request
import requests
import os
# import accountConfig

# 此处填写APIKEY

ACCESS_KEY = '605ccfa99ccd3ff8ccfe9bf25a9a9e05'
SECRET_KEY = '$2a$10$s2PAs2i3TC4PhpwpouPawOtdnSc2E/U/fd9U2Q.rZ4HEZEcFJEgxW'


# API 请求地址
MARKET_URL = "https://api.bitopro.com/v2"
TRADE_URL = "https://api.bitopro.com/v2"

# 首次运行可通过get_accounts()获取acct_id,然后直接赋值,减少重复获取。
ACCOUNT_ID = None

def http_get_request(url, params, add_to_headers=None):
    headers = {}
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    response = requests.get(url, postdata, headers=headers, timeout=25) 
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {}
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params, separators=(',', ':'))
    response = requests.post(url, postdata, headers=headers, timeout=25)
    print(response.json())
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" %(response.text,e))
        return


def api_key_get(params, request_path):
    header = {'X-BITOPRO-APIKEY': ACCESS_KEY}

    host_url = TRADE_URL
    if not params:
        params = {"identity": "john831118@gmail.com", "nonce": int(time.time()*1000)}
    signature, payload = createSign(SECRET_KEY, params)
    header['X-BITOPRO-PAYLOAD'] = payload
    header['X-BITOPRO-SIGNATURE'] = signature
    
    url = host_url + request_path
    return http_get_request(url, params, add_to_headers=header)


def api_key_post(params, request_path):
    header = {'X-BITOPRO-APIKEY': ACCESS_KEY}

    host_url = TRADE_URL
    if not params:
        params = {"identity": "john831118@gmail.com", "nonce": int(time.time()*1000)}
    signature, payload = createSign(SECRET_KEY, params)
    print(payload)
    header['X-BITOPRO-PAYLOAD'] = payload
    header['X-BITOPRO-SIGNATURE'] = signature

    url = host_url + request_path
    return http_post_request(url, params, add_to_headers=header)


def createSign(secret_key, payload):
    payload = json.dumps(payload)
    os.system('node sign.js true '+ "'"+payload+"'")
    fo = open("signature.txt", "r")
    signature = fo.read()
    fo.close()
    fo = open("payload.txt", "r")
    payload = fo.read()
    fo.close()

    return signature, payload
