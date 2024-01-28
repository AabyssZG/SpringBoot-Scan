#!/usr/bin/env python
# coding=utf-8
################
#   AabyssZG   #
################

from inc import output, run, vul, console
import requests, sys, json
from termcolor import cprint
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


# 检查代理的使用
def SpringBoot_Scan_Proxy(args):
    if args.proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': args.proxy},
            "https": "http://%(proxy)s/" % {'proxy': args.proxy}
        }
        cprint(f"=====检测代理可用性中=====", "cyan")
        testurl = "https://www.baidu.com/"
        headers = {"User-Agent": "Mozilla/5.0"}  # 响应头
        try:
            requests.packages.urllib3.disable_warnings()
            res = requests.get(testurl, timeout=10, proxies=proxies, verify=False, headers=headers)
            print(res.status_code)
            # 发起请求,返回响应码
            if res.status_code == 200:
                print("GET www.baidu.com 状态码为:" + str(res.status_code))
                cprint(f"[+] 代理可用，马上执行！", "cyan")
                if args.urlfile:
                    proxies = f'http://{args.proxy}'
                SpringBoot_Scan_Header(args, proxies)

        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except Exception as e:
            print('error:', e)
            cprint(f"[-] 代理不可用，请更换代理！", "magenta")
            sys.exit()
    else:
        proxies = ''
        SpringBoot_Scan_Header(args, proxies)


# 导入自定义HTTP头部
def SpringBoot_Scan_Header(args, proxies):
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
        SpringBoot_Scan_Main(args, proxies, header_new)
    else:
        header_new = '{}'
        SpringBoot_Scan_Main(args, proxies, header_new)


def SpringBoot_Scan_Main(args, proxies, header_new):
    if (args.url or args.urlfile or args.vul or args.vulfile or args.dump or args.zoomeye or args.fofa or args.hunter):
        console.SpringBoot_Scan_console(args, proxies, header_new)
    else:
        output.usage()
        sys.exit()
