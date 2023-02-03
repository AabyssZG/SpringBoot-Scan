#!/usr/bin/env python
# coding=utf-8

from inc import output,run,vul
import sys

# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args,proxies):
    if args.url:
        run.url(args.url,proxies)
    if args.file:
        run.file(args.file,proxies)
    if args.vul:
        vul.vul(args.vul,proxies)
    if args.dump:
        run.dump(args.dump,proxies)
    else:
        output.usage()
        sys.exit()
