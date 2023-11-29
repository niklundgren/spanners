#!/bin/bash
runningn=$( for val in $(sacctmgr list User | grep donadiogrp | awk '{print $1}'); do squeue -u $val ; done | awk '{ if ($6 == "R") { print } }' | awk '{ sum+=$9} END {print sum}' )
runningj=$( for val in $(sacctmgr list User | grep donadiogrp | awk '{print $1}'); do squeue -u $val ; done | awk '{ if ($6 == "R") { print } }' | wc -l )
inquen=$( for val in $(sacctmgr list User | grep donadiogrp | awk '{print $1}'); do squeue -u $val ; done | awk '{ if ($6 == "PD") { print } }' | awk '{ sum+=$9} END {print sum}' )
inquej=$( for val in $(sacctmgr list User | grep donadiogrp | awk '{print $1}'); do squeue -u $val ; done | awk '{ if ($6 == "PD") { print } }' | wc -l )
printf "\nRunning jobs:\n\t${runningj} Jobs using ${runningn} / 17 Nodes\n"
printf "Jobs in queue:\n\t${inquej} Jobs using ${inquen} Nodes\n"

