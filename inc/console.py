#!/usr/bin/env python
# coding=utf-8

from inc import output,run,vul,springcheck
import sys

# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args,proxies):
    if args.url:
        urlnew = springcheck.check(args.url,proxies)
        run.url(urlnew,proxies)
    if args.file:
        run.file(args.file,proxies)
    if args.vul:
        urlnew = springcheck.check(args.vul,proxies)
        vul.vul(urlnew,proxies)
    if args.dump:
        urlnew = springcheck.check(args.dump,proxies)
        run.dump(urlnew,proxies)
    else:
        output.usage()
        sys.exit()
