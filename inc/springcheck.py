#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import hashlib
import sys

from termcolor import cprint

from inc.common import http_get, log_error, merge_headers, normalize_url, exit_interrupt


def Spring_Check(url, proxies, header_new):
    cprint("[.] 正在进行Spring的指纹识别", "cyan")
    Spring_hash = "0488faca4c19046b94d07c3ee83cf9d6"
    Paths = ["favicon.ico", "AabyssZG666"]
    for path in Paths:
        test_url = str(url) + path
        r = http_get(test_url, headers=header_new, proxies=proxies)
        try:
            content_type = r.headers.get("Content-Type", "")
            if r.text and ('timestamp' in r.text):
                cprint("[+] 站点报错内容符合Spring特征，识别成功", "red")
            elif "image" in content_type or "octet-stream" in content_type:
                favicon_hash = hashlib.md5(r.content).hexdigest()
                if favicon_hash == Spring_hash:
                    cprint("[+] 站点Favicon是Spring图标，识别成功", "red")
                else:
                    cprint("[-] 站点指纹不符合Spring特征，可能不是Spring框架", "yellow")
            else:
                cprint("[-] 站点指纹不符合Spring特征，可能不是Spring框架", "yellow")
        except KeyboardInterrupt:
            exit_interrupt()
        except Exception as e:
            print("[-] 发生错误，已记入日志error.log\n")
            log_error(e)


def check(url, proxies, header_new):
    header_new = merge_headers({}, header_new)
    url = normalize_url(url)
    try:
        r = http_get(url, headers=header_new, proxies=proxies)
        if (r.status_code == 503) or (r.status_code == 502):
            cprint("[-] 网页状态码为503或502", "magenta")
            sys.exit()
        else:
            Spring_Check(url, proxies, header_new)
            return url
    except KeyboardInterrupt:
        exit_interrupt()
    except Exception as e:
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！已记入日志error.log", "magenta")
        log_error(e)
        sys.exit()
