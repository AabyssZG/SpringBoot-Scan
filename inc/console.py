#!/usr/bin/env python
# coding=utf-8
  ################
 #   AabyssZG   #
################

from inc import output,run,vul,springcheck,zoom,fofa,poc,hunter
import sys,asyncio

# 控制台-参数处理和程序调用
async def SpringBoot_Scan_console(args, proxies,header_new):

    if args.url:
        inp=input("是否需要进行Spring框架探测？：")
        if inp =="y":
            urlnew = await springcheck.check(args.url, proxies,header_new)
            await run.async_url(urlnew, proxies,header_new)
        if inp =="n":
            await run.async_url(args.url, proxies,header_new)
    if args.urlfile:
        asyncio.run(run.file_main(args.urlfile,proxies,header_new))
    if args.vul:
        urlnew = springcheck.check(args.vul, proxies,header_new)
        vul.vul(urlnew, proxies,header_new)
    if args.vulfile:
        poc.poc(args.vulfile, proxies,header_new)
    if args.dump:
        urlnew = springcheck.check(args.dump, proxies,header_new)
        run.dump(urlnew, proxies,header_new)
    if args.zoomeye:
        zoom.ZoomDowload(args.zoomeye,proxies)
    if args.fofa:
        fofa.FofaDowload(args.fofa,proxies)
    if args.hunter:
        hunter.HunterDowload(args.hunter,proxies)
    else:
        output.usage()
        sys.exit()
