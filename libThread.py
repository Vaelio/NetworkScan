#!/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread, activeCount
from Queue import Queue
from time import sleep


class pool():
    
    def __new__(self, number):
        self.num_of_thread = 2
        return self
 
    def __init(self, number):
        self.num_of_thread = number

    def set_number(self, number):
        self.num_of_thread = number

    def map(self, target_func=False, args_tab=False, daemonize=False):
        returns = []
        queue = Queue()
        for x in range(0, len(args_tab), self.num_of_thread):
            for y in range(x,x+self.num_of_thread):
                try:
                    new_thread = Thread(target = target_func, args=(queue, args_tab[y],)) 
                    new_thread.setDaemon(daemonize)
                    new_thread.start()
                except IndexError:
                    break
            while activeCount() > 1:
                pass
        for x in range(len(args_tab)):
            returns.append(queue.get())
        return returns


