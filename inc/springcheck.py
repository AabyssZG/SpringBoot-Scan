#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,vul,console
import requests, sys, hashlib, json,random,aiohttp
from termcolor import cprint
from aiohttp_socks import ProxyConnector
requests.packages.urllib3.disable_warnings()

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]
async def Spring_Check(url,proxies):
    cprint("[.] 正在进行Spring的指纹识别","cyan")
    Spring_hash = "0488faca4c19046b94d07c3ee83cf9d6"
    Paths = ["favicon.ico", "AabyssZG666"]
    header = {"User-Agent": random.choice(ua)}
    for path in Paths:
        test_url = str(url) + path

        # r = requests.get(test_url, timeout=10, verify=False, headers=header)
        try:
            if proxies == "":
                async with aiohttp.ClientSession(headers=header) as session:
                    async with session.get(test_url, timeout=6, ssl=False) as r:
                        content_type = r.headers.get("Content-Type", "")
                        resp=await r.text()
                        if "image" in content_type or "octet-stream" in content_type:
                            favicon_hash = hashlib.md5(r.content).hexdigest()
                            if favicon_hash == Spring_hash:
                                cprint("[+] 站点Favicon是Spring图标，识别成功","red")
                                break
                        elif resp and ('timestamp' in resp):
                            cprint("[+] 站点报错内容符合Spring特征，识别成功","red")
                            break
                        else:
                            cprint("[-] 站点指纹不符合Spring特征，可能不是Spring框架","yellow")
            else:
                conn = ProxyConnector.from_url(proxies)
                print(proxies)
                async with aiohttp.ClientSession(headers=header,connector=conn) as session:
                    async with session.get(test_url, timeout=6, ssl=False) as r:
                        content_type = r.headers.get("Content-Type", "")
                        resp=await r.text()
                        if "image" in content_type or "octet-stream" in content_type:
                            favicon_hash = hashlib.md5(r.content).hexdigest()
                            if favicon_hash == Spring_hash:
                                cprint("[+] 站点Favicon是Spring图标，识别成功","red")
                                break
                        elif resp and ('timestamp' in resp):
                            cprint("[+] 站点报错内容符合Spring特征，识别成功","red")
                            break
                        else:
                            cprint("[-] 站点指纹不符合Spring特征，可能不是Spring框架","yellow")
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except Exception as e:
            print("[-] 发生错误，已记入日志error.log\n")
            f2 = open("error.log", "a")
            f2.write(str(e) + '\n')
            f2.close()

async def check(url,proxies):
    if ('://' not in url):
        url = str("http://") + str(url)
    if str(url[-1]) != "/":
        url = url + "/"
    header = {"User-Agent": random.choice(ua)}
    # try:
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, timeout=6, verify=False, headers=header)  # 设置超时6秒
    if r.status_code == 503:
        sys.exit()
    else:
        await Spring_Check(url,proxies)
        return url
# except KeyboardInterrupt:
    print("Ctrl + C 手动终止了进程")
    sys.exit()
# except Exception as e:
    print(e)
    cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！已记入日志error.log", "magenta")
    f2 = open("error.log", "a")
    f2.write(str(e) + '\n')
    f2.close()
    sys.exit()
