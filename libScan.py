#!/bin/env python
#-*- coding:utf-8 -*-


from socket import socket, setdefaulttimeout
from socket import error as socket_error
from errno import ECONNREFUSED
from libThread import pool

class host():
    def __init__(self, host_ip):
        self.host_ip = host_ip
        self.open_port = []
        self.closed_port = []
        self.up = False

    def try_port(self, queue, port):
        if type(port) == type('str'):
            port = int(port)
        try:
            socket_obj = socket(2, 1)
            result = socket_obj.connect_ex((self.host_ip, port))
        except socket_error as serr:
            if serr == ECONNREFUSED:
                queue.put('%s:Closed'%port)
        finally:
            socket_obj.close()  
        if result == 0:
            queue.put('%s:Open'%port)
            self.up = True
        elif result == 11:
            self.up = False
            queue.put('%s:HOST IS DEAD'%self.host_ip)
        else:
            queue.put('%s:Closed'%port)
            self.up = True

    def scan_port(self, port_list):
        port_threading_pool = pool()
        port_threading_pool.set_number(16)
        port_list = port_threading_pool.map(self.try_port, port_list)
        for item in port_list:
            if 'Open' in item:
                self.open_port.append(item.split(':')[0])
            elif 'HOST IS DEAD' in item:
                self.up = False
                

def host_discovery(network, port):
    if len(port) <= 10:
        print 'PORT SCAN %s: %s'%(network, port)
    else:
        print 'FULL SCAN %s'%network
    if '/' in network:
        # WE HAVE A NETMASK
        CIDR = int(network.split('/')[1])
        if CIDR == 32:
            host_to_scan = host(network)
            host_to_scan.scan_port(port)
            print 'Host %s has those open port:\n%s' %(network, host_to_scan.open_port)
        else:
            ipbase = '.'.join(network.split('.')[:-1])+'.'
            hostlist = []
            print 'Scanning %d hosts'%(2**(32-CIDR))
            for item in range(1,2**(32-CIDR)-1):
                host_obj = host(ipbase+str(item))
                host_obj.scan_port(port)
                if host_obj.up == True:
                    if host_obj.open_port:
                        print 'Host %s has those open port:\n%s' %(ipbase+str(item), host_obj.open_port)
                    else:
                        print 'Host %s is up but got no open port'%(ipbase+str(item))

    elif '-' in network:
        # WE HAVE RANGE
        exit("Not yet implemented")
    else:
        # WE HAVE SINGLE IP
        host_obj = host(network)
        host_obj.scan_port(port)
        if host_obj.up == True:
            if host_obj.open_port:
                print 'Host %s has those open port:\n%s' %(network, host_obj.open_port)
            else:
                print 'Host %s is up but got no open port'%(network)
        else:
            print  'Host is not up it looks like'
