#!/usr/bin/env python

import socket
import struct 

#TCP_IP = '149.161.238.148'
#TCP_PORT = 6350

TCP_IP = '192.168.56.101'
TCP_PORT = 6343

BUFFER_SIZE = 654

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#send 'u' to COBI studio to complete handshake 
s.sendall(b'u')

while(True):
    data = s.recv(BUFFER_SIZE)
    try:
        data_unpacked = struct.unpack_from('<H54i', data)     
        
        for optode, index_offset in enumerate(range(1, 54, 3), start=1):
            raw_730nm = data_unpacked[index_offset]
            raw_ambient = data_unpacked[index_offset+1]
            raw_850nm = data_unpacked[index_offset+2]
            
            print( optode, raw_730nm, raw_ambient, raw_850nm)
        
    except Exception as error:
        print error
        
        
        data_unpacked = struct.unpack_from('B', data)
        print data_unpacked

s.close()
