#!/usr/bin/env python3
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, run, vul, console
import requests, sys, json,aiohttp,re
from termcolor import cprint

requests.packages.urllib3.disable_warnings()
from aiohttp_socks import ProxyConnector
# 检查代理的使用
async def SpringBoot_Scan_Proxy(args):
    if args.proxy:
        proxies = args.proxy
        conn = ProxyConnector.from_url(proxies)
        cprint(f"=====检测代理可用性中=====", "cyan")
        testurl = "https://www.ipplus360.com/getIP"
        headers = {"User-Agent": "Mozilla/5.0"}  # 响应头

        try:
            async with aiohttp.ClientSession(headers=headers,connector=conn) as session:
                async with session.get(testurl, timeout=6, ssl=False) as r:
                    resp = await r.text()
                    print(r.status)
                    pattern = r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})'
                    ip = re.findall(pattern, resp)
                    print(ip)
            # 发起请求,返回响应码
                    if r.status == 200:
                        print("GET访问页面 状态码为:" + str(r.status))
                        cprint(f"[+] 代理可用，马上执行！", "cyan")
                        if args.urlfile:
                            proxies = args.proxy
                        await SpringBoot_Scan_Header(args, proxies)

                        # await console.SpringBoot_Scan_console(args, proxies)
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except Exception as e:
            # if "Connection reset by peer" or "0 bytes read on a total of 2 expected bytes" in str(e):
            #     cprint(f"[-] 代理不可用，请更换代理！", "magenta")
            # else:
            cprint(f"[-] 出现错误{str(e)}", "magenta")
            sys.exit()
    else:
        await console.SpringBoot_Scan_console(args, "",)
# 导入自定义HTTP头部
async def SpringBoot_Scan_Header(args, proxies):
    if args.newheader:
        cprint(f"=====正在导入自定义HTTP头部=====", "cyan")
        filename = args.newheader
        with open(filename, 'r') as file:
            lines = file.readlines()
        # 创建 JSON 对象
        header_json = {}
        for line in lines:
            # 按照 ':' 分隔每行内容，取前后两部分
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                header_json[key] = value
        header_new = json.dumps(header_json, indent=2)
        print(header_new)
        await SpringBoot_Scan_Main(args, proxies, header_new)
    else:
        header_new = '{}'
        await SpringBoot_Scan_Main(args, proxies, header_new)

async def SpringBoot_Scan_Main(args, proxies,header_new):
    if (args.url or args.urlfile or args.vul or args.vulfile or args.dump or args.zoomeye or args.fofa or args.hunter):
        print(args.url)
        await console.SpringBoot_Scan_console(args, proxies,header_new)

    else:
        output.usage()
        sys.exit()
