 Time Based Control
 1) Set up a timing based control function to draw a 0.5 meter box counterclockwise, once
 2) Set up a timing based control function to draw a 1 meter box clockwise, repeating
 3) Do not use sleep, delay or any other blocking approach to measure time.
 B. Line Follower
 1) Set up a simple line following control, test, and observe the disadvantages of this approach.
 2) Set up a line following control function with a simple memory so that if the vehicle loses the line
 it will turn towards where it last saw the line.
 3) For all tests, if an obstacle is blocking the path, stop at a safe distance.
C. Linear Control
 The goal of this assignment is to create a PID controller to help the uctronics car stop one meter an
 obstacle.
 1) Create a script called pid_controller.py in aut_sys/scripts and implement the follow
ing:
 a) Create a Subscriber that reads from the /distance topic.
 b) Create one publisher that writes into the /motors topic to move the robot.
 c) Set rate = rospy.Rate(10) and use rate.sleep() in a loop to maintain a partic
ular rate for the subscriber callback function. Remember that the rate function defines the
 execution speed of your node. In this particular case, the configured frequency is 10Hz, which
 means that the controller node will be scheduled for execution every 100ms. You can tune this
 parameter, setting it too high will cause an unnecessary load, while setting it to a low value
 can make your controller to respond very slow.
 d) In the callback function, get the distance measured from the ultrasonic sensor, calculate the
 error to the target position, use a PID controller to control the velocity, and then publish the
 velocity (/motors) and position (/distance).
 2) A launch file called run_pid_control.launch will be provided. Copy it into the /launch
 folder. This file will:
 a) Launch the main script pid_controller.py
 b) Run rqt_plot. This node should subscribe to /cmd_vel/linear/x and /distance.
 We use it to monitor the robot’s behavior in a real-time plot.
 3) Launch run_mission.launch. See the response in rqt_plot. Try to make the settling time
 as small as possible by tuning the controller.
