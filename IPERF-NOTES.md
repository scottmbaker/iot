okay so it looks like I was evolving my approach last time I worked on this:

1) the dockerfile isn't used anymore, and I don't deploy it in an aether@home specific way anymore

2) the helm-chart will install the standard iperf container (just use helm install iperf-server iperf-server

3) extract the IP address from the pod that was deployed:

$ kubectl describe pod iperf-server-6c44cbd965-jbrrn | grep -i "IP:"
IP:           192.168.84.45
  IP:           192.168.84.45

4) Run iperf on the pi to that address:
  # measure performance of pi sending to iperf-server
  $ iperf3 -c 192.168.84.45
  Connecting to host 192.168.84.45, port 5201
  [  5] local 192.168.0.10 port 37140 connected to 192.168.84.45 port 5201
  [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
  [  5]   0.00-1.00   sec  1.06 MBytes  8.92 Mbits/sec    0   81.8 KBytes
  [  5]   1.00-2.00   sec  1.17 MBytes  9.79 Mbits/sec    0    132 KBytes
  [  5]   2.00-3.00   sec  1006 KBytes  8.24 Mbits/sec    0    185 KBytes
  [  5]   3.00-4.00   sec  1.35 MBytes  11.3 Mbits/sec    0    238 KBytes
  [  5]   4.00-5.00   sec  1006 KBytes  8.24 Mbits/sec    0    291 KBytes
  [  5]   5.00-6.00   sec  1.11 MBytes  9.27 Mbits/sec    0    343 KBytes
  [  5]   6.00-7.00   sec  1.35 MBytes  11.3 Mbits/sec    0    396 KBytes
  [  5]   7.00-8.00   sec  1006 KBytes  8.24 Mbits/sec    0    450 KBytes
  [  5]   8.00-9.00   sec  1.11 MBytes  9.27 Mbits/sec    0    503 KBytes
  [  5]   9.00-10.00  sec  1.23 MBytes  10.3 Mbits/sec    0    556 KBytes
  - - - - - - - - - - - - - - - - - - - - - - - - -
  [ ID] Interval           Transfer     Bitrate         Retr
  [  5]   0.00-10.00  sec  11.3 MBytes  9.50 Mbits/sec    0             sender
  [  5]   0.00-10.79  sec  10.7 MBytes  8.29 Mbits/sec                  receiver
  iperf Done.
  # measure poerformance of pi receiving from iperf-server
  $ iperf3 -R -c 192.168.84.45
  Connecting to host 192.168.84.45, port 5201
  Reverse mode, remote host 192.168.84.45 is sending
  [  5] local 192.168.0.10 port 37144 connected to 192.168.84.45 port 5201
  [ ID] Interval           Transfer     Bitrate
  [  5]   0.00-1.00   sec  1.16 MBytes  9.72 Mbits/sec
  [  5]   1.00-2.00   sec  1.00 MBytes  8.42 Mbits/sec
  [  5]   2.00-3.00   sec  9.26 MBytes  77.7 Mbits/sec
  [  5]   3.00-4.00   sec  10.7 MBytes  90.1 Mbits/sec
  [  5]   4.00-5.00   sec  10.3 MBytes  86.8 Mbits/sec
  [  5]   5.00-6.00   sec  10.4 MBytes  87.0 Mbits/sec
  [  5]   6.00-7.00   sec  10.4 MBytes  87.4 Mbits/sec
  [  5]   7.00-8.00   sec  10.2 MBytes  85.4 Mbits/sec
  [  5]   8.00-9.00   sec  10.4 MBytes  86.9 Mbits/sec
  [  5]   9.00-10.00  sec  10.1 MBytes  84.6 Mbits/sec
  - - - - - - - - - - - - - - - - - - - - - - - - -
  [ ID] Interval           Transfer     Bitrate         Retr
  [  5]   0.00-10.02  sec  86.8 MBytes  72.6 Mbits/sec    0             sender
  [  5]   0.00-10.00  sec  83.9 MBytes  70.4 Mbits/sec                  receiver
  iperf Done.
  So in this example I got 9.50 Mbps up and 72.6 Mbps down. That's kinda slow.
