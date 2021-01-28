#!/bin/bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# trap : TERM INT
ip route add 10.250.0.0/16 via 192.168.250.3
ethtool -K eth0 tx off rx off gro off gso off
ethtool -K core-rtr-proxy tx off rx off gro off gso off
