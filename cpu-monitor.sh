#!/bin/zsh
# only works in zsh

# time between reading /proc/stat
INTERVAL=1
# log file path
FILE="cpu_usage.log"

# number of cpu cores
CPU_NUM=`cat /proc/stat | grep 'cpu[0-9]' -c` 

if [ ! -f $FILE ]; then
    echo "CPU NUMBER  : $CPU_NUM" >> $FILE
    printf "[TIMESTAMPS] " >> $FILE
    for i in `seq 1 $CPU_NUM`; do
        printf "c%d " $i  >> $FILE
    done
    echo >> $FILE
fi

while :; do
    # array of cpus
    cpuInfo=$(cat /proc/stat | grep "cpu[0-9]")
    startTotalSum=($(echo ${cpuInfo} | awk '{print $2+$3+$4+$5+$6+$7+$8}' | tr "\n" " "))
    startIdleSum=($(echo ${cpuInfo} | awk '{print $5}' | tr "\n" " "))

    sleep $INTERVAL

    # array of cpus
    cpuInfo=$(cat /proc/stat | grep "cpu[0-9]")
    stopTotalSum=($(echo ${cpuInfo} | awk '{print $2+$3+$4+$5+$6+$7+$8}' | tr "\n" " "))
    stopIdleSum=($(echo ${cpuInfo} | awk '{print $5}' | tr "\n" " "))

    for i in `seq 1 $CPU_NUM`; do
        total=$((stopTotalSum[i]-startTotalSum[i]))
        idle=$((stopIdleSum[i]-startIdleSum[i]))
        percentage[$i]=$((100*(total-idle)/total))
    done

    time=$(date +%s)
    printf "[$time] " >> $FILE
    for p in $percentage; do
        printf "%2d " $p >> $FILE
    done
    echo >> $FILE
done