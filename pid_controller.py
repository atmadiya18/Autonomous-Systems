#!/usr/bin/env python3

import rospy, time
from aut_sys.msg import distance, motors
from simple_pid import PID

distant = 0

#data will contain message info from distance
def dist_callback(data):
  global distant
  distant = data.distance
  rospy.loginfo('Received ctr:{}'.format(data.distance))
 
# Function to create a PID controller to help the  car stop 0.5 meter
def controller():
  global distant
  # Motors message published
  pub = rospy.Publisher('/motors', motors, queue_size=10)
  # Node created for the uctronics car
  rospy.init_node('controller', anonymous=True)
  rate = rospy.Rate(10)
  # Kp = 2, Ki = 0.01, Kd = 0.05, setpoint is given as 0.5  
  pid = PID(2, 0.01, 0.05, setpoint=0.5)
  # Output in between the given values
  pid.output_limits = (-1, 1)
  # publishing the velocity
  motors_msg = motors()
  rospy.Subscriber('distance', distance, dist_callback)
  # Executing the loop with the car on
  while not rospy.is_shutdown():
    rospy.loginfo('[controller] Running')    
    # Return the new motor speed
    control = pid(distant)
    # As distance changes from 1 to 0, control -ve  
    motors_msg.leftSpeed = motors_msg.rightSpeed = -control
    pub.publish(motors_msg)
    rospy.loginfo(motors_msg)
    # Maintain 10Hz rate for the Subscriber
    rate.sleep()
   
if __name__ == '__main__':
  try:
    controller()
  except rospy.ROSInterruptException:
    pass