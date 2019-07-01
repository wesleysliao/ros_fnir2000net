#!/usr/bin/env python

import socket


TCP_IP = '149.161.161.56'
TCP_PORT = 6343
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data