#!/bin/bash
set -e
echo "Content-type: text/html"
echo ''
echo "registering pi at $REMOTE_ADDR"

cp /etc/hosts /tmp/hosts_modify
sed -i '/raspi-server/d' /tmp/hosts_modify
echo "$REMOTE_ADDR raspi-server" >> /tmp/hosts_modify
cp /tmp/hosts_modify /etc/hosts
