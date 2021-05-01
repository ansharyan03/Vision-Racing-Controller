from engine import CaptureEngine
import cv2
import pyxinput



# virtual_controller = pyxinput.vController()

webcam = cv2.VideoCapture(1)
webcam.set(3, 1280)
webcam.set(4, 720)
colors = [[104 ,137, 115, 125, 255, 255],
[130, 111, 111, 166, 218, 185]]

ang = 0
temp = 0
while True:
    working, img = webcam.read()
    temp2 = temp
    temp = ang
    ang = CaptureEngine.find_angle(img, colors)
    # if(abs(ang - temp) > 20):
    #     ang = temp + (temp-temp2)
    print(ang)
    # virtual_controller.set_value('AxisLx', ang/90)

    if cv2.waitKey(100) & 0xFF ==ord('q'):
        break