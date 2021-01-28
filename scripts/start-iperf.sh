#!/bin/bash
echo SCRIPT: start-iperf.sh
chmod a+rw /etc/hosts
service apache2 start
iperf3 -s
