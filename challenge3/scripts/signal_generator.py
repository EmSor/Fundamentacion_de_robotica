#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

#funcion de stop
def stop():
    pub.publish(0)
    rate.sleep()
    print("Stopping")


if __name__=='__main__':
    rospy.init_node("signal_generator")
    rate = rospy.Rate(30)

    #se define el publisher de la senial
    pub=rospy.Publisher("signal",Float32, queue_size=10)

    #se define el inicio del tiempo
    t0 = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
        tipo = rospy.get_param("tipo","seno")
        #inicia la funcion que genera el waveform de seno
        if(tipo == "seno"):
            P = rospy.get_param("P",4)
            phase = rospy.get_param("phase",0)
            amplitud = rospy.get_param("amplitud",1)
            offset = rospy.get_param("offset",0)
            w = 2*np.pi/P
            t = rospy.Time.now().to_sec() - t0
            timeset = t
            setout = (np.sin(w*t + phase)*amplitud)+offset
        #inicia la funcion que genera el waveform de square
        elif tipo == "square":
            P = rospy.get_param("P",4)
            phase = rospy.get_param("phase",0)
            amplitud = rospy.get_param("amplitud",1)
            offset = rospy.get_param("offset",0)
            w = 2*np.pi/P
            t = rospy.Time.now().to_sec() - t0
            if(np.sin(w*t+phase)*amplitud)>=0:
                setout = rospy.get_param("tope",1)
                timeset = t
            else:
                setout = rospy.get_param("fondo",-1)
                timeset = t
        #inicia la funcion que genera el waveform de step
        elif tipo == "step":
            P = rospy.get_param("P",4)
            phase = rospy.get_param("phase",0)
            amplitud = rospy.get_param("amplitud",1)
            offset = rospy.get_param("offset",0.7)
            w = 2*np.pi/P
            t = rospy.Time.now().to_sec() - t0
            setout = offset
            timeset = t

        #publica el dato del waveform
        pub.publish(setout)
        #se espera un instante
        rate.sleep()

