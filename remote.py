#!/usr/bin/env python

import sys
import io
import os
import json


#ps -e -o pid,user,pcpu,pmem,command --sort=-pcpu |head

class Remote:
    #get disk usage
    def getDf(self):
        df = os.popen('df')
        return df.read()

    #get load
    def getLoad(self):
        data = open('/proc/loadavg', 'r')
        return data.read()
                   
    #get top prgs
    def getTopLoad(self):
        load = os.popen('ps -e -o pid,user,pcpu,pmem,command --sort=-pcpu |head')
        return load.read()

    #get top mem
    def getTopMem(self):
        mem = os.popen('ps -e -o pid,user,pcpu,pmem,command --sort=-pmem |head')
        return mem.read()
    

    #get time
    def getTime(self):
        time = os.popen('date')
        return time.read()
    

    #get hostname
    def getHostname(self):
        host = os.popen('hostname -f')
        return host.read()
    
    #get all json
    def getAllJson(self):
        all={
            u"time":self.getTime(),
            u"load":self.getLoad(),
            u"hostname":self.getHostname(),
            u"disk":self.getDf(),
            u"topLoad":self.getTopLoad(),
            u"topMem":self.getTopMem(),
            }
        return all

if __name__ == '__main__':
    r=Remote()

    print r.getDf()
    print r.getLoad()
    print r.getTime()
    print r.getAllJson()
