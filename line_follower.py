#!/usr/bin/env python3

import rospy
import time
from aut_sys.msg import motors
from aut_sys.msg import lines
from aut_sys.msg import distance

line_data = [0]*3
dist_data = 0
stop = 0

#store initial starting time
starttime = time.time()

def scan_callback(data):
    global dist_data
    #data will contain message info from distance
    print(data)              #display current distance seen
    dist_data = data.distance

def scan_callback2(data2):
    global line_data
    #data will contain message info from distance
    #print(data2)              #display current distance seen
    line_data[2] = data2.leftLine
    line_data[1] = data2.midLine
    line_data[0] = data2.rightLine

def line_follower_memory():
    global line_data, stop, dist_data
    # Create a publisher object with motors 
    pub = rospy.Publisher('motors', motors, queue_size=10)
    # Declare the node and register it with a name
    rospy.init_node('line_follower', anonymous=True)
    # Execution Rate
    rate = rospy.Rate(20)
    # Define a subcriber to catch distance messages
    rospy.Subscriber("distance", distance, scan_callback)
    # Define a subcriber to catch line follower messages
    rospy.Subscriber("lines", lines, scan_callback2)

    '''
        Main Loop beginning
    '''

    while not rospy.is_shutdown():
        #create message object with motor type
        vel_msg = motors()
        line = line_data
        
        if (stop != 1):
            if (dist_data != 0.0) and (dist_data < 0.25) and ((time.time() - starttime) > 2):
                stop = 1
                print('OBJECT DETECTED')
                vel_msg.leftSpeed = 0
                vel_msg.rightSpeed = 0
            else:         
                if (line[2] == False) and (line[1] == False):
                    vel_msg.leftSpeed = 0
                    vel_msg.rightSpeed = 0.5
                elif (line[2] == False):
                    vel_msg.leftSpeed = -0.325
                    vel_msg.rightSpeed = 0.4
                elif (line[0] == False) and (line[1] == False):
                    vel_msg.leftSpeed = 0.5
                    vel_msg.rightSpeed = 0.0
                elif (line[0] == False):
                    vel_msg.leftSpeed = 0.4
                    vel_msg.rightSpeed = -0.325
                elif (line[1] == False):
                    vel_msg.leftSpeed = 0.29
                    vel_msg.rightSpeed = 0.29
                #elif (line[2] == True) and (line[1] == True) and (line[0] == True):
                #    vel_msg.leftSpeed = 0
                #    vel_msg.rightSpeed = 0
                else:
                    vel_msg.leftSpeed = 0.29
                    vel_msg.rightSpeed = 0.29        
        #log/trance information on console
        rospy.loginfo('[line_follower_memory_node] Running')

        #print(vel_msg)         #printing velocity for debugging purposes
        print(line)            #printing line data for debugging purposes

        #Publish the speed 
        pub.publish(vel_msg)
        #sleep to maintain 10hz rate
        rate.sleep()


if __name__ == '__main__':
    try:
            line_follower_memory()
    except rospy.ROSInterruptException:
        pass