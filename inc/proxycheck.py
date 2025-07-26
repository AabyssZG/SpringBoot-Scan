#!/usr/bin/env python3
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, console
import sys
import requests
from termcolor import cprint
import json
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

def SpringBoot_Scan_Proxy(args):
    proxies = {}
    if args.proxy:
        proxies = {
            "http": f"http://{args.proxy}",
            "https": f"http://{args.proxy}"
        }
        cprint("===== 检测代理可用性中 =====", "cyan")
        test_url = "https://www.baidu.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = requests.get(test_url, headers=headers, proxies=proxies, verify=False, timeout=10)
            if res.status_code == 200:
                cprint(f"[+] 代理可用，马上执行！", "green")
            else:
                cprint(f"[-] 代理不可用，请更换代理！", "red")
                sys.exit()
        except Exception as e:
            cprint(f"[-] 代理连接失败: {e}", "red")
            sys.exit()

    headers = {}
    if args.newheader:
        try:
            with open(args.newheader, 'r', encoding='utf-8') as f:
                headers = json.load(f)
            cprint(f"[+] 成功加载自定义 HTTP 头部文件: {args.newheader}", "green")
        except Exception as e:
            cprint(f"[-] 读取 HTTP 头部文件失败: {e}", "red")
            sys.exit()

    if args.cookie:
        headers['Cookie'] = args.cookie
        cprint(f"[+] 已添加自定义 Cookie 到请求头", "green")

    if args.url or args.urlfile or args.vul or args.vulfile or args.dump or args.zoomeye or args.fofa or args.hunter or args.dumpfile:
        console.SpringBoot_Scan_console(args, proxies, headers)
    else:
        output.usage()
        sys.exit()
        