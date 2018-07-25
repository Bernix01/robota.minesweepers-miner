#!/usr/bin/env python
import time
import serial
import rospy
from std_msgs.msg import Bool
import RPi.GPIO as GPIO


def sensor_pedro():
    # nametopic rospy.Publisher crea el topic y lo guarda en pub
    pub = rospy.Publisher('detection_sensor_pedro', Bool, queue_size=10)
    rospy.init_node('sensor_pedro')  # namenodo
    rate = rospy.Rate(10)  # 10hz #posiblemente lo omita
    valor_min = 300
    valor_max = 500
    b = False
    while b==False:
        try:
            ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            b = True
        except:
            pass
    gpio_foco = rospy.get_param("GPIO_FOCO")
    GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD
    GPIO.setup(gpio_foco, GPIO.OUT)           # set GPIO24 as an output
    while not rospy.is_shutdown():
        data = ser.readline()
        # rospy.loginfo("DATA received:" + data + ", " + str(type(data)))
        try:
            data = float(data)
            # rospy.loginfo("DATA:" + str(data))
            # rospy.loginfo(data >= valor_min and data <= valor_max)
            if (data >= valor_min and data <= valor_max):
                rospy.loginfo("ENCONTRO METAL")
                pub.publish(True)  # pub.publish publica en la variable pub
        except Exception as e:
            rospy.logerr(e.message)
        finally:
            rate.sleep()  # funciona casi como un delay


if __name__ == '__main__':
    try:
        sensor_pedro()
    except rospy.ROSInterruptException:
        pass
