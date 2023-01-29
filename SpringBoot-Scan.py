#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, console, run
import re, binascii, argparse, sys, time

def get_parser():
    parser = argparse.ArgumentParser(usage='python3 SpringBoot-Scan.py',description='SpringBoot-Scan: 针对SpringBoot的开源渗透框架',)
    p = parser.add_argument_group('FileReverse-Tools 的参数')
    p.add_argument("-u", "--url", type=str, help="对单一URL进行信息泄露扫描")
    p.add_argument("-f", "--file", type=str, help="读取目标TXT进行信息泄露扫描")
    p.add_argument("-v", "--vul", type=str, help="对单一URL进行漏洞利用")
    p.add_argument("-d", "--dump", type=str, help="扫描并下载SpringBoot敏感文件（可提取敏感信息）")
    args = parser.parse_args()
    return args

def main():
    output.logo()
    args = get_parser()
    console.SpringBoot_Scan_console(args)

if __name__ == '__main__':
    main()