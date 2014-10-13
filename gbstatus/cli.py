#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import NMClient
import datetime
import libvirt
import socket
import struct
import time
import sys
import os


def network():
    def show_ipv4(i):
        return socket.inet_ntoa(struct.pack("I", i))
    nmc = NMClient.Client.new()
    devs = nmc.get_devices()
    dev_info = {}
    other_info = []
    for dev in devs:
        info = []
        v4 = dev.get_ip4_config()
        if not v4:
            continue
        if isinstance(dev, NMClient.DeviceWifi):
            ap = dev.get_active_access_point()
            if ap is not None:
                info.append(ap.get_ssid())
                info.append("%d%%" % (ap.get_strength()))
        if isinstance(dev, NMClient.DeviceEthernet):
            sp = dev.get_speed()
            if sp >= 1000:
                info.append("%dG" % (sp / 1000))
            else:
                info.append("%dM" % (sp))
        for addr in v4.get_addresses():
            info.append(show_ipv4(addr.get_address()))
        dev_info[dev.get_iface()] = info
    if not nmc.wireless_hardware_get_enabled():
        other_info.append("!wifi_hw")
    elif not nmc.wireless_get_enabled():
        other_info.append("!wifi")
    r = " ".join(k + " " + " ".join(dev_info[k]) for k in sorted(dev_info))
    if other_info:
        r += " " + " ".join(other_info)
    return r


def battery():
    def sys_read(f):
        with open(f) as fd:
            return fd.read()
    sys_read_float = lambda f: float(sys_read(f))
    per = 100 * sys_read_float('/sys/class/power_supply/BAT0/charge_now') / \
        sys_read_float('/sys/class/power_supply/BAT0/charge_full')
    return "⚡ %d%%" % (round(per))


libvirt_conn = libvirt.openReadOnly('lxc:///')


def vms():
    return ' '.join(
        '⌨  ' + t.name() for t in libvirt_conn.listAllDomains()
        if t.isActive())


def load():
    return "😰 %.2f" % (os.getloadavg()[0])


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Status:
    def __init__(self):
        self.sep = ' | '
        self.interval = 5
        self.status_fns = [network, vms, battery, load, now]

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