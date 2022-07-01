import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(0)

while True:
    retval, frame = cap.read()
    if not retval:
        print('error')
        break

    # print('shape:', frame.shape)

    frameHeight, frameWidth = frame.shape[:2]
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ## blue
    lower_blue = (100, 75, 90)
    upper_blue = (150, 255, 255)
    mask_blue = cv2.inRange(frame_hsv, lower_blue, upper_blue)
    result_blue = cv2.bitwise_and(frame, frame, mask_blue)

    ## green
    lower_green = (40, 100, 25)
    upper_green = (95, 255, 255)
    mask_green = cv2.inRange(frame_hsv, lower_green, upper_green)
    result_green = cv2.bitwise_and(frame, frame, mask_green)

    ## black
    # lower_black = (0, 0, 0)
    # upper_black = (10, 25, 25)
    # mask_black = cv2.inRange(frame_hsv, lower_black, upper_black)
    # result_black = cv2.bitwise_and(frame, frame, mask_black)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(3,3))
    erode = cv2.erode(gray, kernel, iterations=5)
    dilate = cv2.dilate(gray, kernel, iterations=5)
    erode2 = cv2.erode(dilate, kernel, iterations=7)
    lower_black = 0
    upper_black = 30
    ret, dst = cv2.threshold(erode2, 70, 255, cv2.THRESH_BINARY)    # +cv2.THRESH_OTSU
    mask_black = cv2.inRange(dst, lower_black, upper_black)
    result_black = cv2.bitwise_and(frame, frame, mask_black)

    ## red
    lower_red = (140, 25, 25)
    upper_red = (190, 255, 255)
    mask_red = cv2.inRange(frame_hsv, lower_red, upper_red)
    result_red = cv2.bitwise_and(frame, frame, mask_red)

    # 파란색 인식
    contours_blue, hierarchy = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_blue) > 0:
        for i in range(len(contours_blue)):
            # Get area value
            area = cv2.contourArea(contours_blue[i])
            if area > 3500:  # minimum blue area
                rect = cv2.minAreaRect(contours_blue[i])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                result_blue = cv2.drawContours(result_blue, [box], -1, (255, 0, 0), 3)

    # 초록색 인식
    contours_green, hierarchy = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_green) > 0:
        for i in range(len(contours_green)):
            # Get area value
            area = cv2.contourArea(contours_green[i])
            if area > 3500:  # minimum area
                rect = cv2.minAreaRect(contours_green[i])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                result_green = cv2.drawContours(result_green, [box], -1, (0, 255, 0), 3)

    # 검은색 인식
    contours_black, hierarchy = cv2.findContours(mask_black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_black) > 0:
        for i in range(len(contours_black)):
            # Get area value
            area = cv2.contourArea(contours_black[i])
            if area > 3500:  # minimum area
                rect = cv2.minAreaRect(contours_black[i])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                result_black = cv2.drawContours(result_black, [box], -1, (255, 255, 255), 3)

    # 빨간색 인식
    contours_red, hierarchy = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_red) > 0:
        for i in range(len(contours_red)):
            # Get area value
            area = cv2.contourArea(contours_red[i])
            if area > 3000:  # minimum area
                rect = cv2.minAreaRect(contours_red[i])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                result_red = cv2.drawContours(result_red, [box], -1, (0, 0, 255), 3)

    # result_black = cv2.bitwise_and(frame, frame, mask_black)

    # cv2.imshow('original', frame)
    cv2.imshow('blue', result_blue)
    cv2.imshow('green', result_green)
    cv2.imshow('black', result_black)
    cv2.imshow('red', result_red)
    cv2.imshow('binary', dst)
    # cv2.imshow('result', result)



    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()
