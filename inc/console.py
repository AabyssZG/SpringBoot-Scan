#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,vul,springcheck,zoom,fofa,poc,hunter
import sys,asyncio

# 控制台-参数处理和程序调用
async def SpringBoot_Scan_console(args, proxies):

    if args.url:
        inp=input("是否需要进行Spring框架探测？：")
        if inp =="y":
            urlnew = await springcheck.check(args.url, proxies)
            await run.async_url(urlnew, proxies)
        if inp =="n":
            await run.async_url(args.url, proxies)
    if args.urlfile:
        asyncio.run(run.file_main(args.urlfile,proxies))
    if args.vul:
        if inp =="y":
            urlnew = springcheck.check(args.vul, proxies)
            vul.vul(urlnew, proxies)
        if inp =="n":
            vul.vul(args.vul, proxies)
    if args.vulfile:
        poc.poc(args.vulfile, proxies)
    if args.dump:
        if inp =="y":
            urlnew = springcheck.check(args.dump, proxies)
            run.dump(urlnew, proxies)
        if inp =="n":
            run.dump(args.dump, proxies)
    if args.zoomeye:
        zoom.ZoomDowload(args.zoomeye,proxies)
    if args.fofa:
        fofa.FofaDowload(args.fofa,proxies)
    if args.hunter:
        hunter.HunterDowload(args.hunter,proxies)
    else:
        output.usage()
        sys.exit()
