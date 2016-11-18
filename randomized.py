#!/usr/bin/env python

import sys
import socket

if len(sys.argv) != 3:
    sys.exit("Usage: %s PORT LISTEN_PORT" % sys.argv[0])

port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

sock.sendall("GET /index.html HTTP/1.0\r\n\r\n")

while True:
    buf = sock.recv(1024)
    if not buf:
        break
    sys.stdout.write(buf)
sock.close()
