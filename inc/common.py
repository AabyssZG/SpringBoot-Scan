#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import json
import random
import string
import sys

import requests
import urllib3

urllib3.disable_warnings()

OUTTIME = 10

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
]


def random_ua():
    return random.choice(UA_LIST)


def merge_headers(base, header_new):
    if not isinstance(header_new, dict):
        header_new = json.loads(header_new) if header_new else {}
    return {**base, **header_new}


def normalize_url(url):
    url = url.strip()
    if '://' not in url:
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"
    return url


def log_error(e):
    with open("error.log", "a") as f:
        f.write(str(e) + '\n')


def write_result(filename, line):
    with open(filename, "a") as f:
        f.write(line + '\n')


def random_string(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def http_get(url, headers=None, proxies=None, **kwargs):
    kwargs.setdefault('timeout', OUTTIME)
    kwargs.setdefault('verify', False)
    kwargs.setdefault('allow_redirects', False)
    return requests.get(url, headers=headers, proxies=proxies, **kwargs)


def http_post(url, headers=None, proxies=None, **kwargs):
    kwargs.setdefault('timeout', OUTTIME)
    kwargs.setdefault('verify', False)
    kwargs.setdefault('allow_redirects', False)
    return requests.post(url, headers=headers, proxies=proxies, **kwargs)


def http_head(url, headers=None, proxies=None, **kwargs):
    kwargs.setdefault('timeout', OUTTIME)
    kwargs.setdefault('verify', False)
    kwargs.setdefault('allow_redirects', False)
    return requests.head(url, headers=headers, proxies=proxies, **kwargs)


def http_delete(url, headers=None, proxies=None, **kwargs):
    kwargs.setdefault('timeout', OUTTIME)
    kwargs.setdefault('verify', False)
    kwargs.setdefault('allow_redirects', False)
    return requests.delete(url, headers=headers, proxies=proxies, **kwargs)


def exit_interrupt():
    print("Ctrl + C 手动终止了进程")
    sys.exit()
