#!/usr/bin/env python

import psutil
import sys
import os
import json

def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class PsUtilRemote:
  def __init__(self,remoteServer,hostname):
#		if hostname == false

    self.remoteServer=remoteServer
    self.hostname=hostname

#get disk usages
  def get_usage(self):
    templ = [{'dev':'%-17s','total':'%8s','used':'%8s','free':'%8s','use':'%5s%%','type':'%9s','mount':'%-17s'}]
    #outPut=[{"Device", "Total", "Used", "Free", "Use ", "Type","Mount"}]
    #outPut=""
    for part in psutil.disk_partitions(all=False):
      if os.name == 'nt':
        if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
#        outPut (templ % (
#            part.device,
#            bytes2human(usage.total),
#            bytes2human(usage.used),
#            bytes2human(usage.free),
#            int(usage.percent),
#            part.fstype,
#            part.mountpoint))

        print([{"dev":part.device,
"used":bytes2human(usage.used),
"total":bytes2human(usage.total),
"free":bytes2human(usage.free),
"use":int(usage.percent),
"type":part.fstype,
"mount":part.mountpoint}])
       # output += temp
     #   print temp
	
    #return outPut
	
#get load
  def get_load(self):
    return psutil.cpu_percent(interval=1, percpu=True)
#get top proccesses

#get net load

#get users
  def get_users(self):
    return psutil.users()

#post to server

if __name__ == '__main__':
	app=PsUtilRemote("localhost","true")
	print app.get_usage()
#	for line in app.get_usage()
#		print line
