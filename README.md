
Add your SS servers to servers.json.
Config (e.g. password) the connection to SS server in test_ss.py

Run forward-tcp.py to run a TCP forwarding server that automaticlaly pick target server based on speed test.

Below is the original README.md

port-forwarder
==============

Simple Python scripts to listen, log and forward network traffic

Usage
-----
* Use forward-tcp.py to forward TCP traffic
* Use forward-udp.py to forward UDP traffic
* Edit the file and set listen_host, listen_port, target_host, target_port
* python forward-*.py
* Output is written to stdout

* proxy.py forwards HTTP traffic

Other Proxies
-------------
* SMTP: python -m smtpd -c DebuggingServer -n localhost:25

