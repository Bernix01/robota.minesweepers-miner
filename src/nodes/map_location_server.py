#!/usr/bin/env python

from minesweepers.srv import *
import rospy

def handler_map_location(req):
    gyroD = rospy.get_param('gyroD')
    gpsD = rospy.get_param('gpsD')
    x_gyro, y_gyro, t_gyro, acurracy_x_gyro, acurracy_y_gyro = gyroD['X_GYRO'], gyroD['Y_GYRO'], gyroD['T_GYRO'], gyroD['ACURRACY_X_GYRO'], gyroD['ACURRACY_Y_GYRO']
    rospy.loginfo("gyroD are %s, %s, %s, %s, %s", x_gyro, y_gyro, t_gyro, acurracy_x_gyro, acurracy_y_gyro)
    x_gps, y_gps, t_gps, acurracy_x_gps, acurracy_y_gps = gpsD['X_GPS'], gpsD['Y_GPS'], gpsD['T_GPS'], gpsD['ACURRACY_X_GPS'], gpsD['ACURRACY_Y_GPS']
    rospy.loginfo("gpsD are %s, %s, %s, %s, %s", x_gps, y_gps, t_gps, acurracy_x_gps, acurracy_y_gps)

    k = 20
    t_gyro = rospy.get_param('gyroD/t_gyro')
    acurracy_x_gyro = rospy.get_param('gyroD/acurracy_x_gyro')
    acurracy_y_gyro = rospy.get_param('gyroD/acurracy_y_gyro')
    t_gps = rospy.get_param('gpsD/t_gps')
    acurracy_x_gps = rospy.get_param('gyroD/acurracy_x_gps')
    acurracy_y_gps = rospy.get_param('gyroD/acurracy_y_gps')
    t_now = rospy.get_rostime()
    rospy.loginfo("Current time %i %i", t_now.secs, t_now.nsecs)
    if not((t_now-t_gyro) < k or (t_now-t_gyro) < k):
        if (acurracy_x_gyro > acurracy_x_gps):
            pub.publish(rospy.get_param('gyroD/x_gyro'), rospy.get_param('gyroD/y_gyro'))
            rospy.loginfo(rospy.get_param('gyroD/x_gyro'), rospy.get_param('gyroD/y_gyro'))
            return {
                " x " : x_gyro,
                " y " : y_gyro,
            }
        else:
            pub.publish(rospy.get_param('gpsD/x_gps'), rospy.get_param('gpsD/y_gps'))
            rospy.loginfo(rospy.get_param('gpsD/x_gps'), rospy.get_param('gpsD/y_gps'))
            return {
                " x " : x_gps,
                " y " : y_gps,
            }
    else:
        pub.publish(x = -1, y = -1)
        rospy.loginfo(x = -1, y = -1)
        return {
                " x " : -1,
                " y " : -1,
            }

def map_location_server():
    rospy.init_node('map_location_server') #inicializamos el nodo de servivio
    s = rospy.Service('map_location', rospy_minesweepers.srv.map_locationRequest, handler_map_location) #declarar el servivio
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        gyroD = rospy.get_param('gyroD')
        gpsD = rospy.get_param('gpsD')
        x_gyro, y_gyro, t_gyro, acurracy_x_gyro, acurracy_y_gyro = gyroD['X_GYRO'], gyroD['Y_GYRO'], gyroD['T_GYRO'], gyroD['ACURRACY_X_GYRO'], gyroD['ACURRACY_Y_GYRO']
        rospy.loginfo("gyroD are %s, %s, %s, %s, %s", x_gyro, y_gyro, t_gyro, acurracy_x_gyro, acurracy_y_gyro)
        x_gps, y_gps, t_gps, acurracy_x_gps, acurracy_y_gps = gpsD['X_GPS'], gpsD['Y_GPS'], gpsD['T_GPS'], gpsD['ACURRACY_X_GPS'], gpsD['ACURRACY_Y_GPS']
        rospy.loginfo("gpsD are %s, %s, %s, %s, %s", x_gps, y_gps, t_gps, acurracy_x_gps, acurracy_y_gps)

        k = 20
        pub = rospy.Publisher(param_talker, String)
        t_gyro = rospy.get_param('gyroD/t_gyro')
        acurracy_x_gyro = rospy.get_param('gyroD/acurracy_x_gyro')
        acurracy_y_gyro = rospy.get_param('gyroD/acurracy_y_gyro')
        t_gps = rospy.get_param('gpsD/t_gps')
        acurracy_x_gps = rospy.get_param('gyroD/acurracy_x_gps')
        acurracy_y_gps = rospy.get_param('gyroD/acurracy_y_gps')
        t_now = rospy.get_rostime()
        rospy.loginfo("Current time %i %i", t_now.secs, t_now.nsecs)
        try:
            if not((t_now-t_gyro) < k or (t_now-t_gyro) < k):
                if (acurracy_x_gyro > acurracy_x_gps):
                    pub.publish(rospy.get_param('gyroD/x_gyro'), rospy.get_param('gyroD/y_gyro'))
                    rospy.loginfo(rospy.get_param('gyroD/x_gyro'), rospy.get_param('gyroD/y_gyro'))
                    return {
                        " x " : x_gyro,
                        " y " : y_gyro,
                    }
                else:
                    pub.publish(rospy.get_param('gpsD/x_gps'), rospy.get_param('gpsD/y_gps'))
                    rospy.loginfo(rospy.get_param('gpsD/x_gps'), rospy.get_param('gpsD/y_gps'))
                    return {
                        " x " : x_gps,
                        " y " : y_gps,
                    }
            else:
                pub.publish(x = -1, y = -1)
                rospy.loginfo(x = -1, y = -1)
                return {
                        " x " : -1,
                        " y " : -1,
                    }
        except Exception as e:
            rospy.logerr(e.message)
        finally:
            rate.sleep()# funciona casi como un delay
    rospy.spin()

if __name__ == "__main__":
    try:
        map_location_server()
    except rospy.ROSInterruptException:
        pass
