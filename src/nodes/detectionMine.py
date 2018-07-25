#!/usr/bin/env python
import rospy
from minesweepers.msg import Detection_parameter
from minesweepers.srv import map_location
from std_msgs.msg import Bool

class Detection():

    topic = None

    def setup(self):
        self.topic = rospy.Publisher(
            'mine_detection', Detection_parameter, queue_size=10)
        rospy.init_node('detectionMine')
        rospy.Subscriber('detection_sensor_pedro', Bool, self.callback)

    def callback(self, data):
        # obtener info del servicio maplocation
        rospy.wait_for_service('map_location')
        try:
            map_location_service = rospy.ServiceProxy(
                'map_location', map_location)
            resp1 = map_location_service()
            self.topic.pub.publish(resp1)
        except rospy.ServiceException, a:
            print "Service call failed: %s" % a


if __name__ == '__main__':
    try:
        nodo = Detection()
        nodo.setup()
    except rospy.ROSInterruptException:
        pass
