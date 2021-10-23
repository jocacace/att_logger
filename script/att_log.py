#!/usr/bin/python3


import rospy
import zmq
import time
import json

from std_msgs.msg import String
from geometry_msgs.msg import Vector3

ctx = zmq.Context()
sock2 = ctx.socket(zmq.SUB)
sock2.connect("tcp://192.168.1.201:5556")
sock2.subscribe("DATA")





def att_pub():
    pub = rospy.Publisher('/mockup/attitude', Vector3, queue_size=1)
    rospy.init_node('att_log', anonymous=True)
    
    att = Vector3()
    first_time = 0
    first = True
    f = open('/tmp/attitude.txt', 'w')
    print("Starting receiver loop ...")
    while not rospy.is_shutdown():
        msg = sock2.recv_string()
        d = json.loads( msg[5:len(msg)] )
        
        
        #print(d['y'])
        mtim = d['time']
        r = d['r']
        p = d['p']
        y = d['y']
        
        if ( first == True ):
           first_time = mtim
           first = False
       
       
        #print( (mtim-first_time) /1000 , " ", r, " ", p, " ", y)
        att.x = r
        att.y = p
        att.z = y
        
        mtim = (mtim-first_time) /1000
        #line = str(mtim), ", ", str(r), ", ", str(p), ", ", str(y), "\n"
        #print(line)
        #f.write( line )
        f.write( str(mtim) )
        f.write( ", " )
        f.write( str(r) )
        f.write( ", " )
        f.write( str(p) )
        f.write( ", " )
        f.write( str(y) )
        f.write( "\n" )
        #f.writelines(str(mtim, ", ", r, ", ", p, ", ", y, "\n"))
        
        pub.publish( att )
        
    f.close()
    sock.close()
    #sock2.close()
    ctx.term()

if __name__ == '__main__':
    try:
        att_pub()
    except rospy.ROSInterruptException:
        pass


#while True:
#    msg = sock2.recv_string()
#
#
#    d = json.loads( msg[5:len(msg)] )
#    print(d['y'])
#    #print( msg[5:   ])
#    #msg2 = sock2.recv_string()
#    #print("Received string: %s ..." % msg2)


      
