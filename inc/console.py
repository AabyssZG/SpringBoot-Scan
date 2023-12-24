#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,vul,springcheck,zoom,fofa,poc,hunter
import sys

# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args,proxies):
    if args.url:
        urlnew = springcheck.check(args.url,proxies)
        run.url(urlnew,proxies)
    if args.urlfile:
        run.file(args.urlfile,proxies)
    if args.vul:
        urlnew = springcheck.check(args.vul,proxies)
        vul.vul(urlnew,proxies)
    if args.vulfile:
        poc.poc(args.vulfile,proxies)
    if args.dump:
        urlnew = springcheck.check(args.dump,proxies)
        run.dump(urlnew,proxies)
    if args.zoomeye:
        zoom.ZoomDowload(args.zoomeye,proxies)
    if args.fofa:
        fofa.FofaDowload(args.fofa,proxies)
    if args.hunter:
        hunter.HunterDowload(args.hunter,proxies)
    else:
        output.usage()
        sys.exit()
