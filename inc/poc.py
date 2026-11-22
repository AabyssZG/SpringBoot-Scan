#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import sys

from termcolor import cprint

from inc import exploits
from inc.common import (OUTTIME, exit_interrupt, http_get, normalize_url,
                        write_result)


def FileRead(filename):
    try:
        f = open(filename)   #打开目标文件
        f.close()
    except FileNotFoundError:
        cprint("未找到同目录下的TXT文件，请确保放在一个目录下", "magenta")   #如果未找到文件，输出错误
        sys.exit()
    except PermissionError:
        cprint("无法读取TXT文件（无权限访问）", "magenta")   #如果发现目标文件无权限，输出错误
        sys.exit()


def detect(choice, url, proxies):
    """运行单个漏洞的批量探测，命中时返回写入 vulout.txt 的记录行，否则返回 None"""
    if choice == 1:
        result = exploits.check_jeespring_2023(url, proxies)
        return "[+] [JeeSpring_2023] " + result["poc"] if result else None
    if choice == 2:
        result = exploits.check_cve_2022_22947(url, proxies)
        return "[+] [CVE-2022-22947] " + url if result else None
    if choice == 3:
        return "[+] [CVE-2022-22963] " + url if exploits.check_cve_2022_22963(url, proxies) else None
    if choice == 4:
        result = exploits.check_cve_2022_22965(url, proxies)
        return "[+] [CVE-2022-22965] " + result["shell"] + "?pwd=tomcat&cmd=whoami" if result else None
    if choice == 5:
        result = exploits.check_cve_2021_21234(url, proxies)
        return f"[+] [CVE-2021-21234-{result['os']}] " + url if result else None
    if choice == 6:
        version = exploits.check_snakeyaml(url, proxies)
        tag = {"1.x": "SnakeYAML_RCE-1", "2.x": "SnakeYAML_RCE-2"}.get(version)
        return f"[+] [{tag}] " + url if tag else None
    if choice == 7:
        version = exploits.check_eureka(url, proxies)
        tag = {"1.x": "Eureka_Xstream-1", "2.x": "Eureka_Xstream-2"}.get(version)
        return f"[+] [{tag}] " + url if tag else None
    if choice == 8:
        result = exploits.check_jolokia(url, proxies)
        if not result or result["type"] == "unknown":
            return None
        tag = "Jolokia-Logback-JNDI-RCE" if result["type"] == "logback" else "Jolokia-Realm-JNDI-RCE"
        return f"[+] [{tag}] " + url
    if choice == 9:
        return "[+] [CVE-2018-1273] " + url if exploits.check_cve_2018_1273(url, proxies) else None
    if choice == 10:
        result = exploits.check_cve_2025_41243(url, proxies)
        return "[+] [CVE-2025-41243] " + url if result else None
    if choice == 11:
        if exploits.check_cve_2024_37084(url, proxies) and exploits.exploit_cve_2024_37084(url, "aaa", proxies):
            return "[+] [CVE-2024-37084] " + url
        return None
    if choice == 12:
        hits = exploits.check_cve_2025_22235(url, proxies)
        return "[+] [CVE-2025-22235] " + url if hits else None
    if choice == 13:
        result = exploits.check_cve_2025_24813(url, proxies)
        return "[+] [CVE-2025-24813] " + url if result and result["write"] else None
    if choice == 14:
        result = exploits.check_cve_2026_59378(url, proxies)
        # 批量模式只记录已确认启用默认鉴权的高置信度命中，降低误报
        if result and result["secured"]:
            return "[+] [CVE-2026-59378] " + url
        return None
    if choice == 15:
        result = exploits.check_cve_2026_47884(url, proxies)
        return "[+] [CVE-2026-47884] " + url if result and result["lfi"] else None
    if choice == 16:
        result = exploits.check_whitelabel_spel(url, proxies)
        return "[+] [Whitelabel_SpEL_RCE] " + result["poc"] if result else None
    return None


def poc(filename, proxies):
    f1 = open("vulout.txt", "wb+")
    f1.close()
    cprint("[+] 获取TXT名字为：" + filename, "green")
    FileRead(filename)
    cprint("[+] 目前漏洞库内容如下：", "green")
    for num, (name, _) in exploits.VULNS.items():
        print(f" {num}: {name}")
    choices = exploits.ask_choices("\n请输入要批量检测的漏洞 (例子：1,3,5 直接回车即检测全部漏洞): ")
    if choices is None:
        print("请不要输入无意义的字符串")
        sys.exit()
    with open(filename, 'r') as temp:
        for url in temp.readlines():
            url = url.strip()
            if not url:
                continue
            url = normalize_url(url)
            try:
                r = http_get(url, proxies=proxies)
                if r.status_code == 503:
                    continue
            except KeyboardInterrupt:
                exit_interrupt()
            except Exception:
                cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
                continue
            for choice in choices:
                if choice not in exploits.VULNS:
                    print(f"{choice} 输入错误，请重新输入漏洞选择模块\n")
                    break
                try:
                    record = detect(choice, url, proxies)
                except KeyboardInterrupt:
                    exit_interrupt()
                if record:
                    cprint(record, "red")
                    write_result("vulout.txt", record)
                else:
                    name = exploits.VULNS[choice][0]
                    cprint(f"[-] 目标 {url} 验证{name}漏洞不存在", "yellow")
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "red")
    sys.exit()
