# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dropout
import cv2
import numpy as np
import math

class CaptureEngine:
    def __init__(self, webcamNum):
        self.webcam = cv2.VideoCapture(webcamNum)
        self.webcam.set(3, 1280)
        self.webcam.set(4, 720)
        self.colors = [[104 ,137, 115, 125, 255, 255],
        [130, 111, 111, 166, 218, 185]]

    def find_contours(self, img, imgCopy):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x,y,w,h = 0,0,0,0
        for contour in contours:
            area = cv2.contourArea(contour)
            # print(area)
            if area > 500:
                cv2.drawContours(imgCopy, contour, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(contour, True)
                #print(peri)
                approx = cv2.approxPolyDP(contour, 0.02*peri, True)
                # print(len(approx))
                obj_cor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
        return x+w//2, y

    def find_color(self, img):
        # h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        # h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        # s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        # s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        # v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        # v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
        # lower = np.array([h_min, s_min, v_min])
        # upper = np.array([h_max, s_max, v_max])
        # lower = np.array([14, 132, 51])
        # upper = np.array([117, 255, 238])
        imgResult = img.copy()
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # cv2.imshow("webcam view", img)
        cv2.imshow("hsv version", imgHSV)
        pos = []
        for i in range(len(self.colors)):
            lower = np.array(self.colors[i][0:3])
            upper = np.array(self.colors[i][3:6])
            mask = cv2.inRange(imgHSV, lower, upper)
            pos.append(self.find_contours(mask, imgResult))
            cv2.imshow(str(i), mask)
        yDiff = pos[1][1] - pos[0][1]
        xDiff = pos[1][0] - pos[0][0]
        slope = yDiff/xDiff if xDiff != 0 else 0
        angle = math.degrees(math.atan(slope))

        # print(pos)
        cv2.imshow("result:", imgResult)
        return angle


    def trackbar_change(self, val):
        pass

    def scan(self):
        # cv2.namedWindow("TrackBars")
        # cv2.resizeWindow("TrackBars",640,480)
        # cv2.createTrackbar("Hue Min", "TrackBars", 0,179, self.trackbar_change)
        # cv2.createTrackbar("Hue Max", "TrackBars", 179,179, self.trackbar_change)
        # cv2.createTrackbar("Sat Min", "TrackBars", 0,255, self.trackbar_change)
        # cv2.createTrackbar("Sat Max", "TrackBars", 255,255, self.trackbar_change)
        # cv2.createTrackbar("Val Min", "TrackBars", 0,255, self.trackbar_change)
        # cv2.createTrackbar("Val Max", "TrackBars", 255,255, self.trackbar_change)

        while True:
            working, img = self.webcam.read()
            ang = self.find_color(img)
            print(ang)

            if cv2.waitKey(100) & 0xFF ==ord('q'):
                break
