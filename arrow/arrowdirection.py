import cv2
import numpy as np
import math

def notion(x):
    pass


src = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX
tmpli = [0,0]
while True:
    _, img = src.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dst = img.copy()

    blur = cv2.GaussianBlur(gray, (5,5), 5)
    canny = cv2.Canny(blur, 100, 200)
    try:
        #콘투어로 가장 큰 직사각형 찾아서 roi 설정
        contours, hier = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        tmp = contours[0]
        x, y, w, h = cv2.boundingRect(tmp)

        cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 255), 3)
        p_center = w/2
        # 음수범위 예외처리
        ry = y - 10
        rx = x - 10
        if ry < 0:
            ry = 0
        if rx < 0:
            rx = 0
        roi1 = canny[ry:y+h+10, rx:x+w+10]
        roi2 = dst[ry:y + h + 10, rx:x + w + 10]
        #### DRAW A CIRCLE ARROUND THE ARROW TO FIND THE ANGLE OF THE ARROW
        # 사실상 안쓰는 코드
        for c in contours:
            # find minimum area
            x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(dst, (x, y), (x + w, y + h), (0, 0, 255), 3)
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            cv2.circle(img, center, 2, (0, 255, 0), 2)
            #cv2.circle(img, (int(am), int(bm)), 2, (0, 255, 0), 2)
    except IndexError:
        pass

    try:
        #코너 찾는 부분
        corners = cv2.goodFeaturesToTrack(roi1, 7, 0.3, 5, blockSize=6, useHarrisDetector=True, k=0.03)
        corners = np.int0(corners)
    except TypeError:
        pass
    try:
        #코너 동그라미
        tmp = 0
        for i in corners:
            cv2.circle(roi2, tuple(i[0]), 3, (0, 255, 0), 2)
            # if tmp == 1:
            #     break
            # tmp += 1
        #코너 좌표값 설정 a = x좌표, b = y좌표
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
        for i in corners[5]:
            a5 = i[0]
            b5 = i[1]
        for i in corners[6]:
            a6 = i[0]
            b6 = i[1]
        # for i in corners[7]:
        #     a7 = i[0]
        #     b7 = i[1]
        # for i in corners[8]:
        #     a8 = i[0]
        #     a8 = i[1]

        am = (a2 + a1) / 2
        bm = (b2 + b1) / 2
        astart = (a5 + a6) / 2
        bstart = (b5 + b6) / 2
        #print(am, bm)
        li_x = [a0,a1,a2,a3,a4,a5,a6] #,a7,a8
        print(li_x)
        cntR = 0
        cntL = 0
        #벽쪽에 붙어있는 corner만 측정
        for i in li_x:
            if i >= p_center+30:
                cntL+=1
            elif i <= p_center-30:
                cntR += 1
        print(p_center)
        print(cntR, cntL)
        if cntR > cntL:
            tmpli[1] += 1
            #print("Right")
        elif cntR < cntL:
            tmpli[0] += 1
            #print("Left")
        # tmpli [0,0]에 왼쪽이면 0번째 인덱스 +1 오른쪽이면 1번째 인덱스 +1
        # 10번 반복해서 가장많은 값 채택
        if sum(tmpli) >= 4:
            if tmpli[0] >= tmpli[1]:
                print("Left")
                
            else:
                print("Right")

            #print("num : ", tmp, x,y)
            #tmp += 1
        # # Drawing lines
        # cv2.line(dst, (int(astart), int(bstart)), (int(am), int(bm)), (0, 255, 0), 1)
        # #cv2.line(dst, center, (int(w), int(h)), (0, 255, 0), 1)
        # print(int(am), int(bm))
        # print(int(w), int(h))
        # # Angles
        # atan = math.atan2(int(bm) - int(bstart), int(am) - int(astart))
        # angle = math.degrees(atan)
        # print('angle=', angle)
        # if (angle >= -90 and angle < 90):
        #     cv2.putText(dst, 'RIGHT', (10, 85), font, 1, (255, 255, 0))
        #     print("RIGHT")
        # # elif (angle >= 45 and angle < 135):
        # #     cv2.putText(dst, 'DOWN', (10, 85), font, 1, (255, 255, 0))
        # #     print("DOWN")
        # elif (angle >= -180 and angle < -90):
        #     cv2.putText(dst, 'LEFT', (10, 85), font, 1, (255, 255, 0))
        #     print("LEFT")
        # elif (angle >= 90 and angle <= 180):
        #     cv2.putText(dst, 'LEFT', (10, 85), font, 1, (255, 255, 0))
        #     print("LEFT")
        # # elif (angle > -135 and angle < -45):
        # #     cv2.putText(dst, 'UP', (10, 85), font, 1, (255, 255, 0))
        # #     print("UP")
    except IndexError:
        pass
    except TypeError:
        pass
    cv2.imshow("roi", roi1)
    cv2.imshow("can", canny)
    cv2.imshow("img", dst)
    cv2.imshow("roi2", roi2)
    cv2.waitKey(25)
cv2.destroyAllWindows()

