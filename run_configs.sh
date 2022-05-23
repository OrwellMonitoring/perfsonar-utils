#!/bin/bash

CONFIG_DIR="./configs"

if [[ $# -eq 0 ]] 
then
    	echo "Missing destination host(s)"
fi


for ip in "$@"
do
	for config in "$CONFIG_DIR"/*
	do
    		$( pscheduler task --archive --import $config --dest $1 & )
	done
done
