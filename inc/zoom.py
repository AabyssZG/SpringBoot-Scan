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
    if ip_port_list == []:
        cprint("[-] 没有搜索到任何资产，请确认你的语法是否正确","yellow")
        sys.exit()
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

def Key_Dowload(key,proxies,choices,searchs):
    cprint("======通过ZoomEye密钥进行API下载数据======","green")
    Headers = {
        "API-KEY": key,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    pagesys = (choices%20)
    pageszc = (choices//20)
    if pagesys > 0:
        pages = pageszc + 1
    else:
        pages = pageszc
    i = 1
    while i <= pages:
        page_url = "&page=" + str(i)
        keyurl = "https://api.zoomeye.org/host/search?query="+ searchs + "&t=web"
        dowloadurl = keyurl + page_url
        cprint("[+] 正在尝试下载第 %d 页数据" % i, "red")
        try:
            requests.packages.urllib3.disable_warnings()
            dowloadre = requests.get(url=dowloadurl, headers=Headers, timeout=6, verify=False, proxies=proxies)
            if (dowloadre.status_code == 200) or (dowloadre.status_code == 201):
                JSON_load(dowloadre.text)
                cprint("-" * 45, "red")
            else:
                cprint("[-] API返回状态码为 %d" % dowloadre.status_code,"yellow")
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

def Key_Test(key,proxies,choices,searchs):
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
            Key_Dowload(key,proxies,choices,searchs)
        else:
            cprint("[-] API返回状态码为 %d" % testre.status_code,"yellow")
            cprint("[-] 请根据返回的状态码，参考官方手册：https://www.zoomeye.org/doc","yellow")
            sys.exit()
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
        choices = input("\n[.] 请输入要测绘的资产数量（默认100条）: ")
        if choices == '':
            choices = "100"
        elif int(choices) <= 0:
            print("请不要输入负数")
            sys.exit()
        choices = int(choices)
    except Exception as e:
        print("请不要输入无意义的字符串")
        sys.exit()
    search = input("[.] 请输入要测绘的语句（默认app:\"Spring Framework\"）: ")
    if search == "":
        searchs = str("app:\"Spring Framework\"")
    else:
        searchs = str(search)
    f2 = open("zoomout.txt", "wb+")
    f2.close()
    Key_Test(key,proxies,choices,searchs)
    count = len(open("zoomout.txt", 'r').readlines())
    if count >= 1:
        cprint("[+][+][+] 已经将ZoomEye的资产结果导出至 zoomout.txt ，共%d行记录" % count,"red")
    sys.exit()
