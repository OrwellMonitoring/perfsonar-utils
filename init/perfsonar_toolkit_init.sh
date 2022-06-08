#!/bin/bash

CONTAINER_NAME=perfsonar
CONTAINER_NAME=perfsonar

docker run --privileged --name $CONTAINER_NAME -v $(pwd)/ntp.conf:/etc/ntp.conf:ro -v /sys/fs/cgroup:/sys/fs/cgroup:ro --net=host -d centos/systemd /usr/sbin/init
docker exec $CONTAINER_NAME yum install -y epel-release
docker exec $CONTAINER_NAME yum install -y http://software.internet2.edu/rpms/el7/x86_64/latest/packages/perfSONAR-repo-0.10-1.noarch.rpm
docker exec $CONTAINER_NAME yum clean all

docker exec $CONTAINER_NAME yum install -y perfsonar-toolkit

docker exec $CONTAINER_NAME esmond_manage add_user_ip_address user 10.0.12.82
