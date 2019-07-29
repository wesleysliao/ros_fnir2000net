#!/usr/bin/env python

import socket
import struct 

import rospy
from ros_fnir2000net.msg import fNIROptode, fNIRArray
from std_msgs.msg import Header

try:
    COBI_Studio_IP = rospy.get_param('COBI_Studio_IP')
    COBI_Studio_PORT = rospy.get_param('COBI_Studio_PORT')
except:
    COBI_Studio_IP = '192.168.56.101'
    COBI_Studio_PORT = 6343

BUFFER_SIZE = 654

#initialze connectino to COBI Studio
cobi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cobi_socket.connect((COBI_Studio_IP, COBI_Studio_PORT))

#send 'u' to COBI Studio to complete handshake 
cobi_socket.sendall(b'u')

#initialize ROS node and publisher
pub = rospy.Publisher('fnir', fNIRArray, queue_size = 10)
rospy.init_node('fnir2000_node', anonymous = True)

def fnir_sender():
    
while True:
    try:
        data = cobi_socket.recv(BUFFER_SIZE)
        data_unpacked = struct.unpack_from('<B54f', data)     
        
        optodelist = []
        for optode, index_offset in enumerate(range(1, 54, 3), start=1):
            raw_730nm = data_unpacked[index_offset]
            raw_ambient = data_unpacked[index_offset+1]
            raw_850nm = data_unpacked[index_offset+2]
            
            fnir_data = [optode, raw_730nm, raw_ambient, raw_850nm]
            print(fnir_data)

        fnirmsg = fNIROptode(raw_730nm = raw_730nm,
                             raw_ambient = raw_ambient,
                             raw_850nm = raw_850nm)
        pub.publish(fnirmsg)
 
    except Exception as error:
        print error
               
s.close()