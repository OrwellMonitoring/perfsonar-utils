#!/bin/bash

docker run -d --net=host --tmpfs /run --tmpfs /tmp -v $(pwd)/ntp.conf:/etc/ntp.conf:ro -v /sys/fs/cgroup:/sys/fs/cgroup:ro perfsonar/testpoint:systemd