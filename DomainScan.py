# !/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import requests
import sys
import Queue
import re

def Argparse():

    parser = argparse.ArgumentParser(usage="%(prog)s [options]",add_help=False,

    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=(u'''
        作者：End1ng blog:end1ng.wordpress.com
        --------------------------------
        domain scan'''))
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-h', '--help', action="store_true", help='help of the %(prog)s program')
    optional.add_argument('--version', action='version', version='%(prog)s 1.1')

    args = parser.add_argument_group('Necessary parameter')

    args.add_argument('-u','--url',metavar=u'url',help=u'目标url')
    args.add_argument('-d','--domain',metavar=u'doma',help=u'网站根域名')

    other = parser.add_argument_group('other arguments')
    other.add_argument('--delay',metavar=u'num',help=u'访问延迟')
    other.add_argument('--cookie',metavar=u'str',help=u'cookie')

    args=parser.parse_args()
    args = vars(args)

    if len(sys.argv) == 1 or args['help']:
        parser.print_help()
        sys.exit()
    if not args['url']:
        print u"请输入url"
        sys.exit()
    if not args["domain"]:
        print u"请输入根域名"
        sys.exit()
    return args

def getlink(url, domain):
    try:
        for u in re.findall("https?://[\w*\.]*[\d:]*", requests.get(url,timeout=3).content):
            if u in urllist or u in faillist:
                pass
            elif re.match("https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:?\d*", u):
                urllist.append(u)
                print "OK " + u
                queue.put(u)
            elif domain in u:
                urllist.append(u)
                print "OK " + u
                queue.put(u)
    except:
        faillist.append(url)
        print "NO " + url

ARGV = Argparse()
queue = Queue.Queue()
urllist = []
faillist = []
queue.put(ARGV['url'])

while not queue.empty():
    getlink(queue.get(), ARGV['domain'])

f = open(ARGV['domain'], "w")
for i in urllist:
    f.write(i + "\n")
f.write("*"*50+"\n")
for i in faillist:
    f.write(i + "\n")