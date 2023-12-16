#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,vul,console
import requests, sys
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
        cprint(f"================检测代理可用性中================", "cyan")
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
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except:
            cprint(f"[-] 代理不可用，请更换代理！", "magenta")
            sys.exit()
    else:
        proxies = ''

    if (args.url or args.file or args.vul or args.dump or args.zoomeye):
        console.SpringBoot_Scan_console(args, proxies)
    else:
        output.usage()
        sys.exit()
