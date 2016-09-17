#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from gi.repository import NMClient
import datetime
import socket
import struct
import time
import sys
import os


def battery():
    def sys_read(f):
        with open(f) as fd:
            return fd.read()
    sys_read_float = lambda f: float(sys_read(f))
    per = 100 * sys_read_float('/sys/class/power_supply/BAT0/charge_now') / \
        sys_read_float('/sys/class/power_supply/BAT0/charge_full')
    return "⚡ %d%%" % (round(per))


def load():
    return "😰 %.2f" % (os.getloadavg()[0])


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Status:
    def __init__(self):
        self.sep = ' | '
        self.interval = 1
        self.status_fns = [battery, load, now]

    def run(self):
        while True:
            self.write_status()
            time.sleep(self.interval)

    def write_status(self):
        line = self.sep.join(filter(None, (t() for t in self.status_fns)))
        sys.stdout.write(line + '\n')
        sys.stdout.flush()


def main():
    Status().run()
