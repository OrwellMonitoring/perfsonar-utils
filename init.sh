CONTAINER_NAME=perfsonar2

docker run --privileged --name $CONTAINER_NAME -v /sys/fs/cgroup:/sys/fs/cgroup:ro --net=host -d centos/systemd /usr/sbin/init
docker exec $CONTAINER_NAME yum install -y epel-release
docker exec $CONTAINER_NAME yum install -y http://software.internet2.edu/rpms/el7/x86_64/latest/packages/perfSONAR-repo-0.10-1.noarch.rpm
docker exec $CONTAINER_NAME yum clean all

docker exec $CONTAINER_NAME yum install -y perfsonar-toolkit

docker exec -it $CONTAINER_NAME bash
