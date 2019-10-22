#!/bin/bash
# only works in bash

# time between reading /proc/stat
INTERVAL=1
# log file path
FILE=$(date +%s)"-cpu_usage.log"

# number of cpu cores
CPU_NUM=$(cat /proc/stat | grep -E 'cpu[0-9]+' | wc -l)

declare -a startTotalSum
declare -a startIdleSum
declare -a stopTotalSum
declare -a stopIdleSum
declare -a percentage

while true; do
  for ((i = 0; i < CPU_NUM; i++)); do
    startTotalSum[$i]=$(cat /proc/stat | grep "cpu$i" | awk \
      '{print $2+$3+$4+$5+$6+$7+$8}')
    startIdleSum[$i]=$(cat /proc/stat | grep "cpu$i" | awk \
      '{print $5}')
  done

  sleep $INTERVAL

  for ((i = 0; i < CPU_NUM; i++)); do
    stopTotalSum[$i]=$(cat /proc/stat | grep "cpu$i" | awk \
      '{print $2+$3+$4+$5+$6+$7+$8}')
    stopIdleSum[$i]=$(cat /proc/stat | grep "cpu$i" | awk \
      '{print $5}')
  done

  for ((i = 0; i < CPU_NUM; i++)); do
    total=$((stopTotalSum[i] - startTotalSum[i]))
    idle=$((stopIdleSum[i] - startIdleSum[i]))
    if [ $total -eq 0 ]; then
      percentage[$i]=0
    else
      percentage[$i]=$((100 * (total - idle) / total))
    fi
  done

  time=$(date +%s)
  printf "$time " >>$FILE
  for ((i = 0; i < CPU_NUM; i++)); do
    printf "%2d " ${percentage[$i]} >>$FILE
  done
  echo >>$FILE
done
