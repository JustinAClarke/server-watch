import atexit
import datetime
import time
import os
import sys

import psutil


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


templ = "%-6s %-8s %4s %5s %5s %6s %4s %9s  %2s"

procs = []
procs_status = {}
psutil.process_iter()
time.sleep(1)
psutil.process_iter()
time.sleep(1)
psutil.process_iter()
time.sleep(1)
psutil.process_iter()
time.sleep(1)
for p in psutil.process_iter():
    try:
        p.dict = p.as_dict(['username', 'nice', 'memory_info',
                            'memory_percent', 'cpu_percent',
                            'cpu_times', 'name', 'status'])
        try:
            procs_status[p.dict['status']] += 1
        except KeyError:
            procs_status[p.dict['status']] = 1
    except psutil.NoSuchProcess:
        pass
    else:
        procs.append(p)


for pro in procs:
    print pro.dict['cpu_percent']
exit()

# processes = sorted(procs, key=lambda p: p.dict['cpu_percent'],
processes = sorted(procs, key=lambda procs:procs.dict['cpu_percent'],
                       reverse=True)

for p in processes:
    # TIME+ column shows process CPU cumulative time and it
    # is expressed as: "mm:ss.ms"
    if p.dict['cpu_times'] is not None:
        ctime = datetime.timedelta(seconds=sum(p.dict['cpu_times']))
        ctime = "%s:%s.%s" % (ctime.seconds // 60 % 60,
                              str((ctime.seconds % 60)).zfill(2),
                              str(ctime.microseconds)[:2])
    else:
        ctime = ''
    if p.dict['memory_percent'] is not None:
        p.dict['memory_percent'] = round(p.dict['memory_percent'], 1)
    else:
        p.dict['memory_percent'] = ''
    if p.dict['cpu_percent'] is None:
        p.dict['cpu_percent'] = ''
    if p.dict['username']:
        username = p.dict['username'][:8]
    else:
        username = ""
    line = templ % (p.pid,
                    username,
                    p.dict['nice'],
                    bytes2human(getattr(p.dict['memory_info'], 'vms', 0)),
                    bytes2human(getattr(p.dict['memory_info'], 'rss', 0)),
                    p.dict['cpu_percent'],
                    p.dict['memory_percent'],
                    ctime,
                    p.dict['name'] or '',
                    )
    print(line)
