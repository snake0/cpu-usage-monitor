#!/usr/bin/python
# merge new data into old data in finish_up

import re
import sys
import os
import signal
import json
import time

# time between reading /proc/stat
INTERVAL = 1
# log file path
FILE = "cpu_usage.json"
# number of cpu cores
CPU_NUM = len(re.findall("cpu[0-9]+", open("/proc/stat").read()))

# dict of log
log = {}


def finish_up(signum, frame):
    global log
    f = open(str(int(time.time())) + "-" + FILE, 'w')
    json.dump(log, f, sort_keys=True, indent=2)
    f.close()
    sys.exit()


def getInfo():
    info = re.findall("cpu[0-9]+ .*", open("/proc/stat").read())
    ret = []
    for i in range(CPU_NUM):
        line = info[i].split(" ")
        ret += [map(int, line[1:])]
    return ret


def main():
    signal.signal(signal.SIGINT, finish_up)
    signal.signal(signal.SIGTERM, finish_up)

    global log
    log = {}
    while True:
        startCpuInfo = getInfo()
        time.sleep(INTERVAL)
        stopCpuInfo = getInfo()

        percentage = []
        for i in range(CPU_NUM):
            total = sum(stopCpuInfo[i]) - sum(startCpuInfo[i])
            idle = stopCpuInfo[i][3] - startCpuInfo[i][3]
            if total != 0:
                percentage.append(100*(total-idle)/total)
            else:
                percentage.append(0)

        log[int(time.time())] = percentage


if __name__ == "__main__":
    main()
