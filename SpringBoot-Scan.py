#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, console, run ,proxycheck
import re, binascii, argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 SpringBoot-Scan.py',description='SpringBoot-Scan: 针对SpringBoot的开源渗透框架',)
    p = parser.add_argument_group('SpringBoot-Scan 的参数')
    p.add_argument("-u", "--url", type=str, help="对单一URL进行信息泄露扫描")
    p.add_argument("-uf", "--urlfile", type=str, help="读取目标TXT进行信息泄露扫描")
    p.add_argument("-v", "--vul", type=str, help="对单一URL进行漏洞利用")
    p.add_argument("-vf", "--vulfile", type=str, help="读取目标TXT进行批量漏洞扫描")
    p.add_argument("-d", "--dump", type=str, help="扫描并下载SpringBoot敏感文件（可提取敏感信息）")
    p.add_argument("-p", "--proxy", type=str, default='', help="使用HTTP代理")
    p.add_argument("-z", "--zoomeye", type=str, default='', help="使用ZoomEye导出Spring框架资产")
    p.add_argument("-f", "--fofa", type=str, default='', help="使用Fofa导出Spring框架资产")
    args = parser.parse_args()
    return args

def main():
    output.logo()
    args = get_parser()
    proxycheck.SpringBoot_Scan_Proxy(args)
    #console.SpringBoot_Scan_console(args)

if __name__ == '__main__':
    main()
