#!/usr/bin/env python
# license removed for brevity
# import rospy
# from minesweepers.msg import Detection
# from minesweepers.srv import SendMessage
# def detectionMine():
#     pub = rospy.Publisher('mine_detection', Detection, queue_size=10)
#     rospy.init_node('detectionMine')
#     rate = rospy.Rate(10) # 10hz cantidad de veces que se ejecuta el bucle
#     rospy.wait_for_service('send_message')
#     while not rospy.is_shutdown():
#         # hello_str = "hello world %s" % rospy.get_time()
#         # rospy.loginfo(hello_str)
#         # pub.publish(hello_str)
#         # rate.sleep()
#         try:
#             send_message = rospy.ServiceProxy('send_message', SendMessage)
#             resp2 = send_message(sensor_data_str)
#         except rospy.ServiceException, a:
#             print "Service call failed: %s"%a
#         rospy.loginfo(sensor_data_str)
#         if pub.get_num_connections() > 0:
#             pub.publish(mine_detection['p'], mine_detection['x'], mine_detection['y'])
#         rate.sleep()
# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  
# def listener():
#     rospy.init_node('listener')
#     #chatter es el topic; el nodo detectionMine esta sub a Spedro y a map_location
#     rospy.Subscriber("chatter", String, callback) 
#     if 
#     rospy.spin()

#/////////////////////////////////////////////////////////////////////////////

import rospy
from minesweepers.msg import Detection_parameter
from minesweepers.srv import map_location

class Detection():

    topic = None

    def setup():
        self.topic = rospy.Publisher('mine_detection', Detection_parameter, queue_size=10)
        rospy.init_node('detectionMine')
        rospy.Subscriber('detection_sensor_pedro', Bool, self.callback) #chatter es el topic; el nodo detectionMine esta sub a Spedro y a map_location

    def callback(data):
        #obtener info del servicio maplocation
        rospy.wait_for_service('map_location')
        try:
            map_location = rospy.ServiceProxy('map_location', rospy_minesweepers.srv.map_locationRequest)
            resp1 = map_location()
            self.topic.pub.publish(resp1)
        except rospy.ServiceException, a:
            print "Service call failed: %s"%a
        
if __name__ == '__main__':
    try:
        nodo = Detection()
        nodo.setup()
    except
        pass
