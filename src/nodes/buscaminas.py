#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Bool
from minesweepers.srv import ComRadio
from minesweepers.msg import Gps
import json


class Buscaminas():
    def __init__(self):
        rospy.Subscriber('detection_sensor_pedro',
                         Bool, self.detection_mine_cb)
        rospy.Subscriber('camera', String, self.camera_cb)
        rospy.Subscriber('gps_data', Gps, self.gps_cb)
        self.send_message = rospy.ServiceProxy('send_message', ComRadio)

    def detection_mine_cb(self, data):
        if self.send_message(action="dm", payload=str(data)):
            rospy.loginfo("Sent detection message!")
        else:
            rospy.logerr("Failed to send detection message!")

    def camera_cb(self, data):
        if self.send_message(action="cm", payload=data.data):
            rospy.loginfo("Sent detection message!")
        else:
            rospy.logerr("Failed to send detection message!")

    def gps_cb(self, data):
        if self.send_message(action="gps", payload=json.dumps(data.data)):
            rospy.loginfo("Sent gps message!")
        else:
            rospy.logerr("Failed to send detection message!")


if __name__ == '__main__':
    try:
        rospy.init_node('buscaminas')
        rospy.wait_for_service('send_message')
        node = Buscaminas()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
