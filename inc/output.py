#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

import time, os, sys

def logo():
    logo0 = r'''
  ______                       __                      _______                        __     
 /      \                     |  \                    |       \                      |  \    
|  $$$$$$\  ______    ______   \$$ _______    ______  | $$$$$$$\  ______    ______  _| $$_   
| $$___\$$ /      \  /      \ |  \|       \  /      \ | $$__/ $$ /      \  /      \|   $$ \  
 \$$    \ |  $$$$$$\|  $$$$$$\| $$| $$$$$$$\|  $$$$$$\| $$    $$|  $$$$$$\|  $$$$$$\\$$$$$$  
 _\$$$$$$\| $$  | $$| $$   \$$| $$| $$  | $$| $$  | $$| $$$$$$$\| $$  | $$| $$  | $$ | $$ __ 
|  \__| $$| $$__/ $$| $$      | $$| $$  | $$| $$__| $$| $$__/ $$| $$__/ $$| $$__/ $$ | $$|  \
 \$$    $$| $$    $$| $$      | $$| $$  | $$ \$$    $$| $$    $$ \$$    $$ \$$    $$  \$$  $$
  \$$$$$$ | $$$$$$$  \$$       \$$ \$$   \$$ _\$$$$$$$ \$$$$$$$   \$$$$$$   \$$$$$$    \$$$$ 
          | $$                              |  \__| $$                                       
          | $$                               \$$    $$   [+] V2.7.1-2025年 欢度国庆佳节版     
           \$$                                \$$$$$$    [+] 感谢一路上支持和关注我们的师傅  
            ______                                                                           
           /      \                                  +-------------------------------------+ 
          |  $$$$$$\  _______  ______   _______      + Version: 2.7.1                      + 
          | $$___\$$ /       \|      \ |       \     + Author: 曾哥(@AabyssZG)             + 
           \$$    \ |  $$$$$$$ \$$$$$$\| $$$$$$$\    + Whoami: https://github.com/AabyssZG + 
           _\$$$$$$\| $$      /      $$| $$  | $$    +-------------------------------------+ 
          |  \__| $$| $$_____|  $$$$$$$| $$  | $$    + 多进程速度提升: Fkalis              + 
           \$$    $$ \$$     \\$$    $$| $$  | $$    + Whoami: github.com/WingBy-Fkalis    + 
            \$$$$$$   \$$$$$$$ \$$$$$$$ \$$   \$$    +-------------------------------------+ 
'''
    print(logo0)

def usage():
    print('''
用法:
        对单一URL进行信息泄露扫描:         python3 SpringBoot-Scan.py -u http://example.com/
        读取目标TXT进行批量信息泄露扫描:   python3 SpringBoot-Scan.py -uf url.txt
        对单一URL进行漏洞扫描:             python3 SpringBoot-Scan.py -v http://example.com/
        读取目标TXT进行批量漏洞扫描：      python3 SpringBoot-Scan.py -vf url.txt
        扫描并下载SpringBoot敏感文件:      python3 SpringBoot-Scan.py -d http://example.com/
        读取目标TXT进行批量敏感文件扫描:   python3 SpringBoot-Scan.py -df url.txt
        使用HTTP代理并自动进行连通性测试:    python3 SpringBoot-Scan.py -p <代理IP:端口>
        从TXT文件中导入自定义HTTP头部:       python3 SpringBoot-Scan.py -t header.txt
        通过ZoomEye密钥进行API下载数据:      python3 SpringBoot-Scan.py -z <ZoomEye的API-KEY>
        通过Fofa密钥进行API下载数据:         python3 SpringBoot-Scan.py -f <Fofa的API-KEY>
        通过Hunter密钥进行API下载数据:       python3 SpringBoot-Scan.py -y <Hunter的API-KEY>

免责声明：
        1.如果您下载、安装、使用、修改本工具及相关代码，即表明您信任本工具
        2.在使用本工具时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任
        3.如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任
        4.请您务必审慎阅读、充分理解各条款内容，特别是免除或者限制责任的条款，并选择接受或不接受
        5.除非您已阅读并接受本协议所有条款，否则您无权下载、安装或使用本工具
        6.您的下载、安装、使用等行为即视为您已阅读并同意上述协议的约束
        ''')

"""
参数:
        -u  --url       对单一URL进行信息泄露扫描
        -uf  --urlfile  读取目标TXT进行批量信息泄露扫描  
        -v  --vul       对单一URL进行漏洞利用
        -vf  --vulfile  读取目标TXT进行批量漏洞扫描
        -d  --dump      扫描并下载SpringBoot敏感文件（可提取敏感信息）
        -df  --dumpfile 读取目标TXT进行批量敏感文件扫描（可提取敏感信息）
        -p  --proxy     使用HTTP进行代理（默认连通性测试www.baidu.com）
        -z  --zoomeye   通过对接ZoomEye的API批量下载Spring的资产测绘数据
        -f  --fofa      通过对接Fofa的API批量下载Spring的资产测绘数据
        -y  --hunter    通过对接Hunter的API批量下载Spring的资产测绘数据
        -t  --newheader 从TXT文件中导入自定义HTTP头部
"""



