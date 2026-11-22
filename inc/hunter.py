#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import base64
import json
import sys
from time import sleep

import requests
from termcolor import cprint

from inc.common import log_error, write_result, exit_interrupt


def JSON_load(text):
    data = json.loads(text)
    if data["data"]["arr"]:
        # 提取ip和port信息
        ip_port_list = [(match["url"]) for match in data["data"]["arr"]]
    else:
        cprint("[-] 没有搜索到任何资产，请确认你的语法是否正确", "yellow")
        sys.exit()
    # 打印提取的信息
    for service in ip_port_list:
        outurl = str(service)
        write_result("hunterout.txt", outurl)
        print(f"Service: {outurl}")


def Key_Dowload(key, proxies, choices, searchs):
    cprint("======通过Hunter密钥进行API下载数据======", "green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    pagesys = (choices % 20)
    pageszc = (choices // 20)
    if pagesys > 0:
        pages = pageszc + 1
    else:
        pages = pageszc
    i = 1
    while i <= pages:
        page_url = "&page=" + str(i)
        keyurl = "https://hunter.qianxin.com/openApi/search?api-key=" + str(key) + "&search=" + str(searchs) + "&page_size=20&is_web=1"
        dowloadurl = str(keyurl + page_url)
        cprint("[+] 正在尝试下载第 %d 页数据" % i, "red")
        try:
            dowloadre = requests.get(url=dowloadurl, headers=Headers, timeout=10, verify=False, proxies=proxies)
            if ("\"code\":200" in str(dowloadre.text)):
                JSON_load(dowloadre.text)
                cprint("-" * 45, "red")
                sleep(2)
            else:
                cprint("[-] API返回状态码为 %d" % dowloadre.status_code, "yellow")
                cprint("[-] 请根据返回的状态码，参考官方手册：https://hunter.qianxin.com/home/helpCenter?r=5-1-1", "yellow")
        except KeyboardInterrupt:
            exit_interrupt()
        except Exception as e:
            print(e)
            print("[-] 发生错误，已记入日志error.log\n")
            log_error(e)
        i = i + 1


def Key_Test(key, proxies, choices, searchs):
    cprint("======您的Hunter密钥进行API对接测试======", "green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    keytesturl = "https://hunter.qianxin.com/openApi/search?api-key=" + key + "&search=dGl0bGU9IuWMl-S6rCI=&page=1&page_size=10&is_web=1"
    try:
        testre = requests.get(url=keytesturl, headers=Headers, timeout=10, verify=False, proxies=proxies)
        data = json.loads(testre.text)
        recode = data["code"]
        if str(recode) == "200":
            cprint("[+] 您的key有效，测试成功！", "red")
            rest_quota = data["data"]["rest_quota"]
            cprint("[+] %s" % rest_quota, "red")
            sleep(2)
            Key_Dowload(key, proxies, choices, searchs)
        else:
            cprint("[-] API返回状态码为 %d" % recode, "yellow")
            cprint("[-] 请根据返回的状态码，参考官方手册：https://hunter.qianxin.com/home/helpCenter?r=5-1-1", "yellow")
            sys.exit()
    except KeyboardInterrupt:
        exit_interrupt()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        log_error(e)


def HunterDowload(key, proxies):
    cprint("======开始对接鹰图接口进行Spring资产测绘======", "green")
    cprint('[+] 您的Hunter密钥为：' + key, "green")
    try:
        choices = input("\n[.] 请输入要测绘的资产数量（默认100条）: ")
        if choices == '':
            choices = "100"
        elif int(choices) <= 0:
            print("请不要输入负数")
            sys.exit()
        choices = int(choices)
    except Exception:
        print("请不要输入无意义的字符串")
        sys.exit()
    search = input("[.] 请输入要测绘的语句（默认app.name=\"Spring Whitelabel Error\"）: ")
    if search == "":
        searchs = str("YXBwLm5hbWU9IlNwcmluZyBXaGl0ZWxhYmVsIEVycm9yIg==")
    else:
        search = base64.urlsafe_b64encode(search.encode("utf-8"))
        searchs = str(search.decode('utf-8'))
    f2 = open("hunterout.txt", "wb+")
    f2.close()
    Key_Test(key, proxies, choices, searchs)
    count = len(open("hunterout.txt", 'r').readlines())
    if count >= 1:
        cprint("[+][+][+] 已经将Hunter的资产结果导出至 hunterout.txt ，共%d行记录" % count, "red")
    sys.exit()
