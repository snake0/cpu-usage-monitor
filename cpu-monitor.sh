#!/bin/zsh
# only works in zsh

# time between reading /proc/stat
INTERVAL=1
# log file path
FILE="cpu_usage.log"

# number of cpu cores
CPU_NUM=`cat /proc/stat | grep 'cpu[0-9]' -c` 

if [ ! -f $FILE ]; then
    echo "CPU number : $CPU_NUM" >> $FILE
    printf "[timestamps]" >> $FILE
    for i in `seq 1 $CPU_NUM`; do
        printf "%2d " 0 >> $FILE
    done
    echo >> $FILE
fi

while true; do
    # array of cpus
    startTotalSum=($(cat /proc/stat | grep "cpu[0-9]" | awk '{print $2+$3+$4+$5+$6+$7+$8}' | tr "\n" " "))
    startIdleSum=($(cat /proc/stat | grep "cpu[0-9]" | awk '{print $5}' | tr "\n" " "))

    sleep $INTERVAL

    # array of cpus
    stopTotalSum=($(cat /proc/stat | grep "cpu[0-9]" | awk '{print $2+$3+$4+$5+$6+$7+$8}' | tr "\n" " "))
    stopIdleSum=($(cat /proc/stat | grep "cpu[0-9]" | awk '{print $5}' | tr "\n" " "))

    for i in `seq 1 $CPU_NUM`; do
        total=$((stopTotalSum[i]-startTotalSum[i]))
        idle=$((stopIdleSum[i]-startIdleSum[i]))
        occupied=$((total-idle))
        occupied_normal=$((occupied*100))
        percentage[$i]=$((occupied_normal/total))
    done

    time=$(date +%s)
    printf "[$time] " >> $FILE
    for p in $percentage; do
        printf "%2d " $p >> $FILE
    done
    echo >> $FILE
done