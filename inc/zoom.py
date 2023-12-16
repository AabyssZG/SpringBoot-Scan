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
    ip_port_list = [(match["portinfo"]["hostname"], match["portinfo"]["service"], match["ip"], match["portinfo"]["port"]) for match in data["matches"]]
    # 打印提取的信息
    for hostname, service, ip, port in ip_port_list:
        if ("https" in service):
            service = "https://"
        else:
            service = "http://"
        if (hostname):
            outurl = str(service) + str(hostname) + ":" + str(port)
        else:
            outurl = str(service) + str(ip) + ":" + str(port)
        f2 = open("zoomout.txt", "a")
        f2.write(str(outurl) + '\n')
        f2.close()
        print(f"Service: {outurl}")

def Key_Dowload(key,proxies,choices):
    cprint("======通过ZoomEye密钥进行API下载数据======","green")
    Headers = {
        "API-KEY": key,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    pages = (choices//20) + 1
    i = 1
    f2 = open("zoomout.txt", "wb+")
    f2.close()
    while i <= pages:
        page_url = "&page=" + str(i)
        keyurl = "https://api.zoomeye.org/host/search?query=app:\"Spring Framework\"&t=web"
        dowloadurl = keyurl + page_url
        cprint("[+] 正在尝试下载第 %d 页数据" % i, "red")
        try:
            requests.packages.urllib3.disable_warnings()
            dowloadre = requests.get(url=dowloadurl, headers=Headers, timeout=6, verify=False, proxies=proxies)
            if (dowloadre.status_code == 200) or (testre.status_code == 201):
                JSON_load(dowloadre.text)
                cprint("-" * 45, "red")
            else:
                cprint("[-] API返回状态码为 %d" % testre.status_code,"yellow")
                cprint("[-] 请根据返回的状态码，参考官方手册：https://www.zoomeye.org/doc","yellow")
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
    cprint("======您的ZoomEye密钥进行API对接测试======","green")
    Headers = {
        "API-KEY": key,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    keytesturl = "https://api.zoomeye.org/host/search?query=app:\"Spring Framework\"&page=1"
    try:
        requests.packages.urllib3.disable_warnings()
        testre = requests.get(url=keytesturl, headers=Headers, timeout=6, verify=False, proxies=proxies)
        if (testre.status_code == 200) or (testre.status_code == 201):
            cprint("[+] 您的key有效，测试成功！", "red")
            Key_Dowload(key,proxies,choices)
        else:
            cprint("[-] API返回状态码为 %d" % testre.status_code,"yellow")
            cprint("[-] 请根据返回的状态码，参考官方手册：https://www.zoomeye.org/doc","yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def ZoomDowload(key,proxies):
    cprint("======开始对接ZoomEye接口进行Spring资产测绘======","green")
    cprint('[+] 您的ZoomEye密钥为：' + key ,"green")
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
    Key_Test(key,proxies,choices)
    count = len(open("zoomout.txt", 'r').readlines())
    if count >= 1:
        cprint("[+][+][+] 已经将ZoomEye的资产结果导出至 zoomout.txt ，共%d行记录" % count,"red")
    sys.exit()