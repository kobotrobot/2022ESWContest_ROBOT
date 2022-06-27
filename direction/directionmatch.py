import cv2, numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
while True:
    retval, frame = cap.read()
    if not retval:
        break

    imgw = cv2.imread('wwwww.jpg')
    imgn = cv2.imread('nnnnn.jpg')
    imge = cv2.imread('eeeee.jpg')
    imgs = cv2.imread('sssss.jpg')
    imgv = frame.copy()
    grayw = cv2.cvtColor(imgw, cv2.COLOR_BGR2GRAY)
    grayn = cv2.cvtColor(imgn, cv2.COLOR_BGR2GRAY)
    graye = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)
    grays = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
    grayv = cv2.cvtColor(imgv, cv2.COLOR_BGR2GRAY)
    # ORB, BF-Hamming 로 knnMatch  ---①
    detector = cv2.ORB_create()
    kpw, descw = detector.detectAndCompute(grayw, None)
    kpn, descn = detector.detectAndCompute(grayn, None)
    kpe, desce = detector.detectAndCompute(graye, None)
    kps, descs = detector.detectAndCompute(grays, None)
    kpv, descv = detector.detectAndCompute(grayv, None)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
    matchesw = matcher.knnMatch(descw, descv, 2)
    matchesn = matcher.knnMatch(descn, descv, 2)
    matchese = matcher.knnMatch(desce, descv, 2)
    matchess = matcher.knnMatch(descs, descv, 2)

    # 이웃 거리의 75%로 좋은 매칭점 추출---②
    ratio = 0.85
    good_matchesw = [first for first,second in matchesw \
                        if first.distance < second.distance * ratio]
    good_matchesn = [first for first,second in matchesn \
                        if first.distance < second.distance * ratio]
    good_matchese = [first for first,second in matchese \
                        if first.distance < second.distance * ratio]
    good_matchess = [first for first,second in matchess \
                        if first.distance < second.distance * ratio]


    m = [len(good_matchesw)/ len(matchesw),len(good_matchesn)/ len(matchesn),len(good_matchese)/ len(matchese),len(good_matchess)/ len(matchess)]

    if max(m) == len(good_matchesw)/len(matchesw):
        good_matches = good_matchesw
        img1 = imgw
        kp1=kpw
        img2 = imgv
        kp2=kpv
        print("w")
    elif max(m) == len(good_matchesn)/len(matchesn):

        good_matches = good_matchesn
        img1 = imgn
        kp1=kpn
        img2 = imgv
        kp2=kpv
        print("N")
    elif max(m) == len(good_matchese)/len(matchese):

        good_matches = good_matchese
        img1 = imge
        kp1=kpe
        img2 = imgv
        kp2=kpv
        print("E")
    elif max(m) == len(good_matchess)/len(matchess):

        good_matches = good_matchess
        img1 = imgs
        kp1=kps
        img2 = imgv
        kp2=kpv
        print("S")
    #print('good matches:%d/%d' %(len(good_matches),len(matches)))


    cv2.imshow('1', imgv)
    key = cv2.waitKey(25)
    if key == 27:
        break
if cap.isOpened():
    cap.release()
    cv2.destroyAllWindows()
