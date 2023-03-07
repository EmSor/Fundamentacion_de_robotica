#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import motor_output
from pid_control.msg import motor_input
from pid_control.msg import set_point


#Setup parameters, vriables and callback functions here (if required)
kp = rospy.get_param("/kp", 0)
ki = rospy.get_param("/ki", 0)
kd = rospy.get_param("/kd", 0)
dt = 0.01
u = 0

mtr_output = 0
mtr_time = 0
mtr_status = 0

sp_input = 0
sp_time = 0

error = 0
sm_error = 0
df_error = 0
error_ant = 0

ctrl_output = motor_input()

def mtr_output_callback(msg):
   global mtr_output, mtr_time, mtr_status
   mtr_output = msg.output
   mtr_time = msg.time
   mtr_status = msg.status

def sp_callback(msg):
   global sp_input, sp_time
   sp_input = msg.set_point
   sp_time = msg.time

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)
    
    #Setup Publishers and subscribers here
    ctrl_out = rospy.Publisher("/motor_input", motor_input, queue_size = 10)
    rospy.Subscriber("/motor_output", motor_output, mtr_output_callback)
    rospy.Subscriber("/set_point", set_point, sp_callback)

    print("The Controller is Running")
    #Run the node
    while not rospy.is_shutdown():

        #Write your code here
        error = sp_input - mtr_output
        sm_error += error * dt
        df_error = (error - error_ant) / dt
        u = kp * error + ki * sm_error + kd * df_error
        ctrl_output.input = u
        ctrl_output.time = rospy.get_time()
        ctrl_out.publish(ctrl_output)
        error_ant = error

        rate.sleep() 
