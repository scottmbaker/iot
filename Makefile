images: rtsp-proxy rtsp-direct udp-proxy iperf

rtsp-proxy:
	docker build -t smbaker/rtsp-proxy:test -f Dockerfile.aether .

rtsp-direct:
	docker build -t smbaker/rtsp-direct:test -f Dockerfile.direct .

udp-proxy:
	docker build -t smbaker/udp-proxy:test -f Dockerfile.udp .

iperf:
	docker build -t smbaker/iperf:test -f Dockerfile.iperf .

publish:
	docker push smbaker/rtsp-proxy:test
	docker push smbaker/rtsp-direct:test
	docker push smbaker/udp-proxy:test
	docker push smbaker/iperf:test
