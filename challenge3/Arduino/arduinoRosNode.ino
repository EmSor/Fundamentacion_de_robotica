#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>
#include <math.h>

#define BUTTON 8
#define LED 13

ros::NodeHandle node_handle;

std_msgs::Float32 signal_msg;

//se declara la funcion de calback para la senial
void subscriberCallback(const std_msgs::Float32& signal_msg) {
  //se convierte la senial a valores en el rango de -255 a 255
  int set_point = signal_msg.data*255;
  //si la senial es positiva gira en un sentido y viceversa
  if (set_point > 0) {
    digitalWrite(3,HIGH);
    digitalWrite(4,LOW);
  } else {
    digitalWrite(3,LOW);
    digitalWrite(4,HIGH);
  }
  //se escribe el valor de pwm
  analogWrite(2,set_point);
}

//se declara el nodo suscriptor
ros::Subscriber<std_msgs::Float32> motor_subscriber("signal", &subscriberCallback);

void setup()
{ 
  //se definen los parametros iniciales
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);

  node_handle.initNode();
  node_handle.subscribe(motor_subscriber);
}

void loop()
{ 
  //ros
  node_handle.spinOnce();
  delay(1);
}
