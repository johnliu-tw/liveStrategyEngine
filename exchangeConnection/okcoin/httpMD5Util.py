#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 用于进行http请求，以及MD5加密，生成签名的工具类

import hashlib
import hmac
import urllib
import json
from urllib.parse import urljoin
from urllib.parse import urlencode

import os
import requests
import traceback 


def buildMySign(params, secretKey):
    s = hashlib.sha1()
    s.update(secretKey.encode('utf-8'))
    h = s.hexdigest()
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    signature = hmac.new(
                    bytes(h, 'latin-1'),
                    msg=bytes(sign[:-1],'latin-1'),
                    digestmod=hashlib.sha256
                ).hexdigest().upper()

    return signature


def httpGet(url, resource, params=''):
    '''
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource + '?' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)
    '''
    try: 
        params = urlencode(params)
        fullURL = urljoin(url, resource + "?" + params)
        print(fullURL)
        response = requests.get(fullURL, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("httpGet failed, detail is:%s" % response.text)
    except requests.ReadTimeout:
        return "Timeout"
    except Exception as e:
        traceback.print_exc()
        return "Error"


def httpPost(url, resource, params, url_params={}):
    '''
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection(url, timeout=10)
    temp_params = urllib.parse.urlencode(params)
    conn.request("POST", resource, temp_params, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    params.clear()
    conn.close()
    return json.loads(data)
    '''
    headers = {
        "Content-type": "application/json",
    }
    try: 
        fullURL = urljoin(url, resource)

        url_params = urllib.parse.urlencode(url_params)
        fullURL += "?" + url_params
        print(fullURL)
        response = requests.post(fullURL, json=params, headers=headers, timeout=80)
        print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("httpPost failed, detail is:%s" % response.text)
    except requests.ReadTimeout:
        return "Timeout"
    except Exception as e:
        traceback.print_exc()
        return "Error"
