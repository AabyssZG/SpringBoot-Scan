#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import base64
import json
import sys

import requests
from termcolor import cprint

from inc.common import log_error, write_result, exit_interrupt


def JSON_load(text):
    data = json.loads(text)
    # 提取ip和port信息
    ip_port_list = [service[0] for service in data["results"]]
    # 打印提取的信息
    if ip_port_list == []:
        cprint("[-] 没有搜索到任何资产，请确认你的语法是否正确", "yellow")
        sys.exit()
    for service in ip_port_list:
        if ("https" not in service):
            service = "http://" + service
        outurl = str(service)
        write_result("fofaout.txt", outurl)
        print(f"Service: {outurl}")


def Key_Dowload(key, proxies, choices, searchs):
    cprint("======通过Fofa密钥进行API下载数据======", "green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    pagesys = (choices % 100)
    pageszc = (choices // 100)
    if pagesys > 0:
        pages = pageszc + 1
    else:
        pages = pageszc
    i = 1
    while i <= pages:
        page_url = "&page=" + str(i)
        keyurl = "https://fofa.info/api/v1/search/all?&key=" + key + "&qbase64=" + str(searchs)
        dowloadurl = keyurl + page_url
        cprint("[+] 正在尝试下载第 %d 页数据" % i, "red")
        try:
            dowloadre = requests.get(url=dowloadurl, headers=Headers, timeout=10, verify=False, proxies=proxies)
            if ("\"error\":false" in str(dowloadre.text)):
                JSON_load(dowloadre.text)
                cprint("-" * 45, "red")
            else:
                cprint("[-] API返回状态码为 %d" % dowloadre.status_code, "yellow")
                cprint("[-] 请根据返回的状态码，参考官方手册：https://fofa.info/api", "yellow")
        except KeyboardInterrupt:
            exit_interrupt()
        except Exception as e:
            print("[-] 发生错误，已记入日志error.log\n")
            log_error(e)
        i = i + 1


def Key_Test(key, proxies, choices, searchs):
    cprint("======您的Fofa密钥进行API对接测试======", "green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    keytesturl = "https://fofa.info/api/v1/info/my?key=" + key
    try:
        testre = requests.get(url=keytesturl, headers=Headers, timeout=6, verify=False, proxies=proxies)
        data = json.loads(testre.text)
        error = data["error"]
        if error == 0:
            username = str(data["username"])
            cprint("[+] 您的key有效，测试成功！您的账号为 %s" % username, "red")
            isvip = data["isvip"]
            if isvip == 1:
                cprint("[+] 您的账号为VIP会员", "red")
            else:
                cprint("[.] 您的账号不是VIP会员", "yellow")
            Key_Dowload(key, proxies, choices, searchs)
        else:
            apierror = data["errmsg"]
            cprint("[-] 发生错误，API返回结果为 %s" % apierror, "yellow")
            cprint("[-] 请根据返回的结果，参考官方手册：https://fofa.info/api", "yellow")
            sys.exit()
    except KeyboardInterrupt:
        exit_interrupt()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        log_error(e)


def FofaDowload(key, proxies):
    cprint("======开始对接Fofa接口进行Spring资产测绘======", "green")
    cprint('[+] 您的Fofa密钥为：' + key, "green")
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
    search = input("[.] 请输入要测绘的语句（默认icon_hash=\"116323821\"||body=\"Whitelabel Error Page\"）: ")
    if search == "":
        searchs = str("aWNvbl9oYXNoPSIxMTYzMjM4MjEifHxib2R5PSJXaGl0ZWxhYmVsIEVycm9yIFBhZ2Ui")
    else:
        search = base64.b64encode(search.encode("utf-8"))
        searchs = str(search.decode('utf-8'))
    f2 = open("fofaout.txt", "wb+")
    f2.close()
    Key_Test(key, proxies, choices, searchs)
    count = len(open("fofaout.txt", 'r').readlines())
    if count >= 1:
        cprint("[+][+][+] 已经将Fofa的资产结果导出至 fofaout.txt ，共%d行记录" % count, "red")
    sys.exit()
