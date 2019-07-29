#!/usr/bin/env python

import socket
import struct 

import rospy
from ros_fnir2000net.msg import fNIROptode, fNIRArray
from std_msgs.msg import Header

TCP_IP = '192.168.56.101'
TCP_PORT = 6343

BUFFER_SIZE = 654

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#send 'u' to COBI studio to complete handshake 
s.sendall(b'u')

def fnir_sender():
    pub = rospy.Publisher('fnir', fNIROptode, queue_size = 10)
    rospy.init_node('fnir2000_node', anonymous = True)
    fnirmsg = fNIROptode(raw_730nm = raw_730nm,
                         raw_ambient = raw_ambient,
                         raw_850nm = raw_850nm)
    pub.publish(fnirmsg)
    
while True:
    try:
        data = s.recv(BUFFER_SIZE)
        print data
        data_unpacked = struct.unpack_from('<B54f', data)     
        
        optodelist = []
        for optode, index_offset in enumerate(range(1, 54, 3), start=1):
            raw_730nm = data_unpacked[index_offset]
            #code0 = data_unpacked[index_offset+1] 
            raw_ambient = data_unpacked[index_offset+1]
            #code1 = data_unpacked[index_offset+3] 
            raw_850nm = data_unpacked[index_offset+2]
            #code2 = data_unpacked[index_offset+5]
            
            fnir_data = [optode, raw_730nm, raw_ambient, raw_850nm]
            print(fnir_data)
            fnir_sender()
 
    except Exception as error:
        print error
               
s.close()
