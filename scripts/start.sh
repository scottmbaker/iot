#!/bin/bash
chmod a+rw /etc/hosts
service apache2 start
rtsp-simple-server
