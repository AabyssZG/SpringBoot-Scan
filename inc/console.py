#!/usr/bin/env python
# coding=utf-8

from inc import output,run,vul
import sys

# 控制台-参数处理和程序调用
def SpringBoot_Scan_console(args):
    if args.url:
        run.url(args.url)
    if args.file:
        run.file(args.file)
    if args.vul:
        vul.vul(args.vul)
    if args.dump:
        run.dump(args.dump)
    else:
        output.usage()
        sys.exit()