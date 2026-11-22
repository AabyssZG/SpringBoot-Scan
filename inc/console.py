#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output, run, vul, springcheck, zoom, fofa, poc, hunter
import sys
import asyncio


# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args, proxies, header_new):
    if args.url:
        urlnew = springcheck.check(args.url, proxies, header_new)
        run.url(urlnew, proxies, header_new)
    elif args.urlfile:
        asyncio.run(run.file_main(args.urlfile, proxies, header_new))
    elif args.vul:
        urlnew = springcheck.check(args.vul, proxies, header_new)
        vul.vul(urlnew, proxies, header_new)
    elif args.vulfile:
        poc.poc(args.vulfile, proxies)
    elif args.dump:
        urlnew = springcheck.check(args.dump, proxies, header_new)
        run.dump(urlnew, proxies, header_new)
    elif args.dumpfile:
        run.dumpfile(args.dumpfile, proxies, header_new)
    elif args.zoomeye:
        zoom.ZoomDowload(args.zoomeye, proxies)
    elif args.fofa:
        fofa.FofaDowload(args.fofa, proxies)
    elif args.hunter:
        hunter.HunterDowload(args.hunter, proxies)
    else:
        output.usage()
        sys.exit()
