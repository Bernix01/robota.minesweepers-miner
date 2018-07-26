#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import time
import json
from std_msgs.msg import String
from picamera.array import PiRGBArray
from picamera import PiCamera


def camera():
    lowerBound = np.array([0, 0, 0])
    upperBound = np.array([349, 70, 30])

    kernelOpen = np.ones((5, 5), np.uint8)
    kernelClose = np.ones((20, 20), np.uint8)
    # initialize the camera and grab a reference to the raw camera capture
    cam = PiCamera()

    # allow the camera to warmup
    time.sleep(0.1)
    rate = rospy.Rate(2)  # 10hz

    while not rospy.is_shutdown():
        pub = rospy.Publisher('camera', String, queue_size=10)
        rospy.init_node('camera')
        # grab an image from the camera
        rawCapture = PiRGBArray(cam)
        cam.capture(rawCapture, format="bgr")
        img = rawCapture.array
        img = cv2.resize(img, (640, 480))
        # convert BGR to HSV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV, lowerBound, upperBound)
        # bitwise and
        res = cv2.bitwise_and(img, img, mask=mask)
        # morphology
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
        maskFinal = maskClose
        cpy = maskFinal.copy()
        _, conts, h = cv2.findContours(
            cpy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        frame_data = []
        for i in range(len(conts)):
            x, y, w, h = cv2.boundingRect(conts[i])
            frame_data.append(x)
            frame_data.append(y)
            frame_data.append(w)
            frame_data.append(h)
        pub.publish(json.dumps(frame_data))
        rate.sleep()


if __name__ == '__main__':
    try:
        camera()
    except rospy.ROSInterruptException:
        pass
