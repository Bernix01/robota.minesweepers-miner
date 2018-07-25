#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from minesweepers.msg import Detection_parameter
from minesweepers.srv import ComRadio
import json


class Buscaminas():
    def __init__(self):
        rospy.Subscriber('detection_sensor_pedro',
                         Detection_parameter, self.detection_mine_cb)
        rospy.Subscriber('camera', Detection_parameter, self.camera_cb)
        self.send_message = rospy.ServiceProxy('send_message', SendMessage)

    def detection_mine_cb(self, data):
        if self.send_message(action="dm",payload=json.dumps(data)):
            rospy.loginfo("Sent detection message!")
        else:
            rospy.logerr("Failed to send detection message!")

    def camera_cb(self, data):
        if self.send_message(action="cm",payload=json.dumps(data)):
            rospy.loginfo("Sent detection message!")
        else:
            rospy.logerr("Failed to send detection message!")


if __name__ == '__main__':
    try:
        rospy.init_node('buscaminas')
        rospy.wait_for_service('send_message')
        rospy.wait_for_node('camera')
        rospy.wait_for_node('detection_sensor_pedro')
        node = Buscaminas()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
