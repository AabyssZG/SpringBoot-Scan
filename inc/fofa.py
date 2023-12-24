#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import requests, sys, json, re, random, base64
from termcolor import cprint
from time import sleep
import urllib3
urllib3.disable_warnings()

def JSON_load(text):
    json_str = text
    data = json.loads(json_str)
    # 提取ip和port信息
    ip_port_list = [service[0] for service in data["results"]]
    # 打印提取的信息
    for service in ip_port_list:
        if ("https" not in service):
            service = "http://" + service
        outurl = str(service)
        f2 = open("fofaout.txt", "a")
        f2.write(str(outurl) + '\n')
        f2.close()
        print(f"Service: {outurl}")

def Key_Dowload(key,proxies,choices):
    cprint("======通过Fofa密钥进行API下载数据======","green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
        }
    pagesys = (choices%100)
    pageszc = (choices//100)
    if pagesys > 0:
        pages = pageszc + 1
    else:
        pages = pageszc
    i = 1
    while i <= pages:
        page_url = "&page=" + str(i)
        keyurl = "https://fofa.info/api/v1/search/all?&key=" + key + "&qbase64=aWNvbl9oYXNoPSIxMTYzMjM4MjEifHxib2R5PSJXaGl0ZWxhYmVsIEVycm9yIFBhZ2Ui"
        dowloadurl = keyurl + page_url
        cprint("[+] 正在尝试下载第 %d 页数据" % i, "red")
        try:
            requests.packages.urllib3.disable_warnings()
            dowloadre = requests.get(url=dowloadurl, headers=Headers, timeout=10, verify=False, proxies=proxies)
            if (dowloadre.status_code == 200) or (dowloadre.status_code == 201):
                JSON_load(dowloadre.text)
                cprint("-" * 45, "red")
            else:
                cprint("[-] API返回状态码为 %d" % dowloadre.status_code,"yellow")
                cprint("[-] 请根据返回的状态码，参考官方手册：https://fofa.info/api","yellow")
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except Exception as e:
            print("[-] 发生错误，已记入日志error.log\n")
            f2 = open("error.log", "a")
            f2.write(str(e) + '\n')
            f2.close()
        i = i + 1

def Key_Test(key,proxies,choices):
    cprint("======您的Fofa密钥进行API对接测试======","green")
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded"
        }
    keytesturl = "https://fofa.info/api/v1/info/my?key=" + key
    try:
        requests.packages.urllib3.disable_warnings()
        testre = requests.get(url=keytesturl, headers=Headers, timeout=6, verify=False, proxies=proxies)
        json_str = testre.text
        data = json.loads(json_str)
        error = data["error"]
        if error == 0:
            username = str(data["username"])
            cprint("[+] 您的key有效，测试成功！您的账号为 %s" % username, "red")
            isvip = data["isvip"]
            if isvip == 1:
                cprint("[+] 您的账号为VIP会员", "red")
            else:
                cprint("[.] 您的账号不是VIP会员", "yellow")
            Key_Dowload(key,proxies,choices)
        else:
            apierror = data["errmsg"]
            cprint("[-] 发生错误，API返回结果为 %s" % apierror,"yellow")
            cprint("[-] 请根据返回的结果，参考官方手册：https://fofa.info/api","yellow")
            sys.exit()
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def FofaDowload(key,proxies):
    cprint("======开始对接Fofa接口进行Spring资产测绘======","green")
    cprint('[+] 您的Fofa密钥为：' + key ,"green")
    try:
        choices = input("\n请输入要测绘的资产数量（默认100条）: ")
        if choices == '':
            choices = "100"
        elif int(choices) <= 0:
            print("请不要输入负数")
            sys.exit()
        choices = int(choices)
    except Exception as e:
        print("请不要输入无意义的字符串")
        sys.exit()
    f2 = open("fofaout.txt", "wb+")
    f2.close()
    Key_Test(key,proxies,choices)
    count = len(open("fofaout.txt", 'r').readlines())
    if count >= 1:
        cprint("[+][+][+] 已经将Fofa的资产结果导出至 fofaout.txt ，共%d行记录" % count,"red")
    sys.exit()
