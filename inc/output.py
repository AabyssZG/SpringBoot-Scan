#!/usr/bin/env python
# coding=utf-8

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
          | $$                               \$$    $$                                       
           \$$                                \$$$$$$                                        
            ______                                                                           
           /      \                                                                          
          |  $$$$$$\  _______  ______   _______      +-------------------------------------+ 
          | $$___\$$ /       \|      \ |       \     +                                     + 
           \$$    \ |  $$$$$$$ \$$$$$$\| $$$$$$$\    + Version: 2.22                       + 
           _\$$$$$$\| $$      /      $$| $$  | $$    + Author: 曾哥(@AabyssZG)             + 
          |  \__| $$| $$_____|  $$$$$$$| $$  | $$    + Whoami: https://github.com/AabyssZG + 
           \$$    $$ \$$     \\$$    $$| $$  | $$    +                                     + 
            \$$$$$$   \$$$$$$$ \$$$$$$$ \$$   \$$    +-------------------------------------+ 
                                                                                             
                                                                                             
'''
    print(logo0)

def usage():
    print('''
用法:
        对单一URL进行信息泄露扫描:         python3 SpringBoot-Scan.py -u http://example.com/
        读取目标TXT进行批量信息泄露扫描:    python3 SpringBoot-Scan.py -uf url.txt
        对单一URL进行漏洞扫描:             python3 SpringBoot-Scan.py -v http://example.com/
        读取目标TXT进行批量漏洞扫描：      python3 SpringBoot-Scan.py -vf url.txt
        扫描并下载SpringBoot敏感文件:      python3 SpringBoot-Scan.py -d http://example.com/
        使用HTTP代理并自动进行连通性测试:    python3 SpringBoot-Scan.py -p <代理IP:端口>
        通过ZoomEye密钥进行API下载数据:      python3 SpringBoot-Scan.py -z <ZoomEye的API-KEY>
        通过Fofa密钥进行API下载数据:         python3 SpringBoot-Scan.py -f <Fofa的API-KEY>

参数:
        -u  --url       对单一URL进行信息泄露扫描
        -uf  --urlfile  读取目标TXT进行批量信息泄露扫描  
        -v  --vul       对单一URL进行漏洞利用
        -vf  --vulfile  读取目标TXT进行批量漏洞扫描
        -d  --dump      扫描并下载SpringBoot敏感文件（可提取敏感信息）
        -p  --proxy     使用HTTP进行代理（默认连通性测试www.baidu.com）
        -z  --zoomeye   通过对接ZoomEye的API批量下载Spring的资产测绘数据
        -f  --fofa      通过对接Fofa的API批量下载Spring的资产测绘数据
        ''', end='')
