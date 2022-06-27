import cv2
import numpy as np
import math

def notion(x):
    pass


cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dst = img.copy()

    blur = cv2.GaussianBlur(gray, (5,5), 5)
    canny = cv2.Canny(blur, 100, 255)

    corners = cv2.goodFeaturesToTrack(canny, 8, 0.01, 5, blockSize=6, useHarrisDetector=True, k=0.03)

    try:
        corners = np.int0(corners)
    except TypeError:
        pass
    try:
        for i in corners:
            cv2.circle(dst, tuple(i[0]), 3, (0, 0, 255), 2)

        for i in corners[0]:
            a0 = i[0]
            b0 = i[1]
        for i in corners[1]:
            a1 = i[0]
            b1 = i[1]
        for i in corners[2]:
            a2 = i[0]
            b2 = i[1]
        for i in corners[3]:
            a3 = i[0]
            b3 = i[1]
        for i in corners[4]:
            a4 = i[0]
            b4 = i[1]

        am = (a0 + a1) / 2
        bm = (b0 + b1) / 2
        #print(am, bm)

        contours, hier = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        #### DRAW A CIRCLE ARROUND THE ARROW TO FIND THE ANGLE OF THE ARROW
        for c in contours:
            # find minimum area
            x, y, w, h = cv2.boundingRect(c)
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            cv2.circle(img, center, 2, (0, 255, 0), 2)
            cv2.circle(img, (int(am), int(bm)), 2, (0, 255, 0), 2)

        # Drawing lines
        cv2.line(img, center, (int(am), int(bm)), (255, 0, 0), 1)
        cv2.line(img, center, (int(radius + x), int(y)), (255, 0, 0), 1)

        # Angles
        atan = math.atan2(int(bm) - int(y), int(am) - int(x))
        angle = math.degrees(atan)
        print('angle=', angle)
        if (angle >= -90 and angle < 90):
            cv2.putText(dst, 'RIGHT', (10, 85), font, 1, (255, 255, 0))
            print("RIGHT")
        # elif (angle >= 45 and angle < 135):
        #     cv2.putText(dst, 'DOWN', (10, 85), font, 1, (255, 255, 0))
        #     print("DOWN")
        elif (angle >= -180 and angle < -90):
            cv2.putText(dst, 'LEFT', (10, 85), font, 1, (255, 255, 0))
            print("LEFT")
        elif (angle >= 90 and angle <= 180):
            cv2.putText(dst, 'LEFT', (10, 85), font, 1, (255, 255, 0))
            print("LEFT")
        # elif (angle > -135 and angle < -45):
        #     cv2.putText(dst, 'UP', (10, 85), font, 1, (255, 255, 0))
        #     print("UP")
    except IndexError:
        pass
    except TypeError:
        pass

    cv2.imshow("can", canny)
    cv2.imshow("img", dst)
    cv2.waitKey(25)
cv2.destroyAllWindows()

