#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import set_point

# Setup Variables, parameters and messages to be used (if required)
hz = rospy.get_param("/rate", 0)
amp = rospy.get_param("/amp", 0)

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(hz)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    sp = rospy.Publisher("set_point", set_point, queue_size = 10)
    
    print("The Set Point Genertor is Running")

    #Run the node
    while not rospy.is_shutdown():

        #Write your code here
        msg = set_point()
        msg.time = rospy.get_time()
        msg.set_point = amp*np.sin(rospy.get_time())
        sp.publish(msg)
        rate.sleep()
