#!/bin/env python
#-*- coding:utf-8 -*-
''' init stuff and launch function from libScan and libThread '''

from argparse import ArgumentParser
from socket import setdefaulttimeout
from libScan import host_discovery

def init():
    ''' Parse Argument and launch functions from libScan and libThread '''
    parser = ArgumentParser(description='Network Scanner by Archelio',\
version='Network Scanner v0.5')
    parser.add_argument('-p', '--port', help='port to scan (Ex: 1 - 5, 6)')
    parser.add_argument('-f', '--full', action='store_true',\
help='defines if you want classic scan or full one')
    parser.add_argument('-t', '--target', \
help='host to scan (Ex: 192.168.1.1, 192.168.1.5-10, 192.168.1.0/24)')
    parser.add_argument('-T', '--timeout', help='changes timeout for socket', type=float)
    args_namespace = parser.parse_args()
    if args_namespace.target is None:
        exit('Please use -h to see usage')
    # HANDLE TIMEOUT
    if args_namespace.timeout is None:
        setdefaulttimeout(0.1)
    else:
        setdefaulttimeout(args_namespace.timeout)
    # HANDLE PORT LIST TO SCAN
    if args_namespace.full and args_namespace.port :
        exit('Can\'t use --full with --port')
    elif args_namespace.full:
        port_list = range(1, 1025)
    elif args_namespace.port:
        if '-' in args_namespace.port and ',' in args_namespace.port:
            port_list = []
            for item in args_namespace.port.split(','):
                if '-' in item:
                    for bounds in range(int(item.split('-')[0]),\
int(item.split('-')[1])+1):
                        port_list.append(bounds)
                else:
                    port_list.append(int(item))
        elif '-' in args_namespace.port:
            port_list = range(int(args_namespace.port.split('-')[0]),\
int(args_namespace.port.split('-')[1])+1)
        elif ',' in args_namespace.port:
            port_list = [int(i) for i in args_namespace.port.split(',')]
        else:
            port_list = [args_namespace.port]
    else:
        port_list = [21, 22, 25, 53, 80, 443, 8000, 8080, 8081, 8443]
    # HANDLE HOST LIST TO SCAN
    if ',' in args_namespace.target:
        for item in args_namespace.target.split(','):
            host_discovery(item, port_list)
    else:
        # target = 192.168.0/24 OU target = 10.10.10.10
        host_discovery(args_namespace.target, port_list)
if __name__ == '__main__':
    try:
        init()
    except KeyboardInterrupt:
        exit(0)
