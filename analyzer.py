#!/usr/bin/python
import os
import re
import sys

# file descriptor of log files
logFiles = []
# minimum time elapsed among all log files
# data beyond that time will be discarded
minTimeElapsed = sys.maxsize
# raw data get from log files, len(allData) == len(logFiles)
allData = []
# number of cpu cores, set in `getAllData`
cpunum = 0


def loadLogFiles():
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
            print("Empty log file.")
            continue

        for line in lines:
            words = line.split()
            percentage = map(int, words[1:])
            data.append((int(words[0]), percentage))
        allData.append(data)

    cpunum = len(allData[0][0][1])


def getMinTimeElapsed():
    global allData, minTimeElapsed
    for data in allData:
        timeElapsed = data[-1][0] - data[0][0]
        if timeElapsed < minTimeElapsed:
            minTimeElapsed = timeElapsed


def fillInData(arr1, arr2):
    global cpunum
    data = []
    for i in range(cpunum):
        data.append((arr1[i] + arr2[i]) / 2)
    return data


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
                newData.append(
                    (prevTime + 1, fillInData(data[j-1][1], data[j][1])))
            newData.append(data[j])
            prevTime = data[j][0]

        allData[i] = newData


def getResult():
    global allData, cpunum
    avg, stddev, gini = [], [], [] # array of cpus

    for i in range(cpunum):
        avg.append(0)    
        stddev.append(0)    
        gini.append(0)    
    
    logLen = 0
    for data in allData:
        logLen += len(data)
        
    for i in range(cpunum):
        for j in range(len(allData)):
            for k in range(len(allData[j])):
                _avg


def printData():
    global allData
    for data in allData:
        for t in data:
            print(t)


def main():
    loadLogFiles()
    getAllData()
    getMinTimeElapsed()
    cleanseData()
    printData()
    getResult()
    finishUp()


if __name__ == "__main__":
    main()
