#!/usr/bin/env python3

import rospy
import time
from aut_sys.msg import motors


#Time delays for various movement
rightTurn = 0.605
leftTurn = 0.6
halfFront = 1
fullFront = 1.75

CW = 0

def time_control():
    global rightTurn, leftTurn, halfFront, fullFront, CW
    
    # Create a publisher object with motors 
    pub = rospy.Publisher('motors', motors, queue_size=10)
    # Declare the node and register it with a name
    rospy.init_node('time_control', anonymous=True)
    # Execution Rate
    rate = rospy.Rate(10)

    '''
        Main Loop beginning
    '''

    while not rospy.is_shutdown():
        #create message object with motor type
        vel_msg = motors()

        #populate motor message object with correct speed
        #Move CCW once
        x = 0
        while x < 4:
            print('While Loop Starting')
            checkpoint = time.time()
            while (time.time() - checkpoint) < halfFront:
                vel_msg.leftSpeed = 0.425
                vel_msg.rightSpeed = 0.425
                pub.publish(vel_msg)
                #sleep to maintain 10hz rate
                rate.sleep()
            checkpoint = time.time()
            while (time.time() - checkpoint) < leftTurn:        
                vel_msg.leftSpeed = -0.65
                vel_msg.rightSpeed = 0.65
                pub.publish(vel_msg)
                #sleep to maintain 10hz rate
                rate.sleep()
            x = x + 1
        
        #Move CW Forever
        y = True       
        while y:
            checkpoint = time.time()
            while (time.time() - checkpoint) < fullFront:
                vel_msg.leftSpeed = 0.425
                vel_msg.rightSpeed = 0.425
                pub.publish(vel_msg)
                #sleep to maintain 10hz rate
                rate.sleep()
            checkpoint = time.time()
            while (time.time() - checkpoint) < leftTurn:        
                vel_msg.leftSpeed = 0.7
                vel_msg.rightSpeed = -0.7
                pub.publish(vel_msg)
                #sleep to maintain 10hz rate
                rate.sleep()
        
        #log/trance information on console
        rospy.loginfo('[time_control_node] Running')

        #Publish the speed 
        #print(vel_msg)         #printing velocity for debugging purposes
        pub.publish(vel_msg)
        #sleep to maintain 10hz rate
        rate.sleep()


if __name__ == '__main__':
    try:
            time_control()
    except rospy.ROSInterruptException:
        pass