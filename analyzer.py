#!/usr/bin/python
# only works in python2
import os
import sys
import math

# data beyond that time will be discarded
minTimeElapsed = sys.maxsize

# file descriptor of log files
logFiles = []
# raw data get from log files
allData = []
# number of cpu cores, set in `getAllData`
cpunum = []


# len(allData) == len(logFiles) == len(cpunum)

def openLogFiles():
    global logFiles
    for i in range(1, len(sys.argv)):
        if not os.path.isfile(sys.argv[i]):
            print("Invalid file name ", sys.argv[i])
        logFiles.append(open(sys.argv[i], 'r'))

    if len(logFiles) == 0:
        print("No log file found. exit")
        sys.exit()


def finishUp():
    global logFiles
    map(lambda f: f.close(), logFiles)


def getAllData():
    global logFiles, allData, cpunum
    for f in logFiles:
        data = []
        lines = f.readlines()
        if len(lines) == 0:
            print("Empty log file. exit")
            sys.exit()

        for line in lines:
            if not line.strip():
                continue
            words = line.split()
            percentage = map(int, words[1:])
            data.append((int(words[0]), percentage))

        allData.append(data)
        cpunum.append(len(data[0][1]))


def getMinTimeElapsed():
    global allData, minTimeElapsed
    for data in allData:
        timeElapsed = data[-1][0] - data[0][0]
        if timeElapsed < minTimeElapsed:
            minTimeElapsed = timeElapsed


def fillInData(line1, line2):
    data = []
    if not len(line1[1]) == len(line2[1]):
        print("Fill in data failed. exit")
        sys.exit()

    for i in range(len(line1[1])):
        data.append((line1[1][i] + line2[1][i]) // 2)
    return (line1[0] + line2[0]) // 2, data


def cleanseData():
    global allData, logFiles, minTimeElapsed

    for i in range(len(logFiles)):
        data = allData[i]
        startTime = data[0][0]
        endTime = startTime + minTimeElapsed
        prevTime = startTime

        newData = [data[0]]
        for j in range(1, len(data)):
            if data[j][0] > endTime:
                break
            if data[j][0] == prevTime + 2:
                newData.append(fillInData(data[j - 1], data[j]))
            newData.append(data[j])
            prevTime = data[j][0]

        allData[i] = newData


# calculate gini coefficient of arr
def gini(arr):
    # values must be positive
    _min = min(arr)
    if _min < 0:
        for i in range(len(arr)):
            arr[i] -= _min
    # values cannot be 0
    for i in range(len(arr)):
        arr[i] += 0.0000001

    # array must be sorted
    arr.sort()
    _len = len(arr)
    _sum_b = sum(arr)
    _sum_a = 0
    for i in range(len(arr)):
        _sum_a += 1.0 * (2 * i - _len + 1) * arr[i]
    return _sum_a / _sum_b / _len


def avg(arr):
    return 0 if len(arr) == 0 else 1.0 * sum(arr) / len(arr)


def stddev(arr):
    if len(arr) == 0:
        return 0

    _stddev = 0
    _avg = avg(arr)
    for i in range(len(arr)):
        diff = arr[i] - _avg
        _stddev += diff * diff

    _stddev /= len(arr)
    _stddev = math.sqrt(_stddev)
    return _stddev


def getResult():
    global allData, cpunum
    # average percentage of each cpu
    avgs = []
    for i in range(len(allData)):
        data = allData[i]
        for j in range(cpunum[i]):
            _sum = 0
            for line in data:
                _sum += line[1][j]
            avgs.append(1.0 * _sum / len(data))

    # print("Average percentage of each cpu:")
    # print("  " + str(avgs))
    print("Average percentage of all %d cpus:" % (sum(cpunum)))
    print("  " + str(avg(avgs)) + "%")
    print("Stddev of percentage of all %d cpus:" % (sum(cpunum)))
    print("  " + str(stddev(avgs)))
    print("Gini coefficient of percentage of all cpus:")
    print("  " + str(gini(avgs)))


def printData():
    global allData
    for data in allData:
        for t in data:
            print(t)


def main():
    openLogFiles()
    getAllData()
    getMinTimeElapsed()
    cleanseData()
    # printData()
    getResult()
    finishUp()


if __name__ == "__main__":
    main()
