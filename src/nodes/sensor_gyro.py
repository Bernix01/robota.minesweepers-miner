#!/usr/bin/env python
import rospy
from minesweepers.msg import Gyro
from mpu6050 import mpu6050
from minesweepers.srv import SendMessage
import time

def sensor_gyro():
    pub = rospy.Publisher('gyro_data', Gyro, queue_size=10)
    rospy.init_node('sensor_gyro')
    rate = rospy.Rate(10) # 10hz
    sensor = mpu6050(0x68)
    start = time.time()
    while not rospy.is_shutdown():
        accelerometer_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        curr_time = time.time()
        sensor_data_str = str(accelerometer_data['x']) + "," + str(accelerometer_data['y']) + "," + str(accelerometer_data['z']) + "," + str(curr_time - start)
        # try:
        #     send_message = rospy.ServiceProxy('send_message', SendMessage)
        #     resp1 = send_message(sensor_data_str)
        # except rospy.ServiceException, e:
        #     print "Service call failed: %s"%e
        rospy.loginfo(sensor_data_str)
        
        if pub.get_num_connections() > 0:
            pub.publish(gyro_data['x'],gyro_data['y'], gyro_data['z'])
        rate.sleep()

if __name__ == '__main__':
    try:
        sensor_gyro()
    except rospy.ROSInterruptException:
        pass