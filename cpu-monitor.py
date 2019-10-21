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
    oldLog = {}
    if os.path.isfile(FILE):
        oldLog = json.load(open(FILE))

    global log
    f = open(FILE, 'w')
    newLog = dict(oldLog, **log)
    json.dump(newLog, f, sort_keys=True, indent=2, separators=(", ", ": "))
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

        log[int(time.time())] = str(percentage)


if __name__ == "__main__":
    main()
