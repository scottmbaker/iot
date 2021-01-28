#!/bin/bash
chmod a+rw /etc/hosts
service apache2 start
while [[ 1 ]]; do
    socat UDP4-RECVFROM:1234,fork UDP4-SENDTO:raspi-server:1234
    sleep 1
done
