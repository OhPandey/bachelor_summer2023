import cv2
import numpy as np
from matplotlib import pyplot as plt

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class WindowsClosed(Exception):
    ...
    pass


def writeText(frame, text):
    # Text Settings
    font = cv2.QT_FONT_NORMAL
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2

    # Bounderies of text
    textsize = cv2.getTextSize(text, font, 1, 2)[0]

    # Position it correctly on the top center
    textX = (frame.shape[1] - textsize[0]) // 2
    textY = textsize[1] + 10

    frame = cv2.putText(frame, text, (textX, textY), font,
                        fontScale, color, thickness, cv2.LINE_AA)
    return frame


def templatematching(frame, windowname):
    img1 = cv2.imread('card.jpg', 0)
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=1000)

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.72 * n.distance:
            good.append([m])

    if len(good) >= 15:
        faces = face_cascade.detectMultiScale(img2, 1.1, 4)
        frame = writeText(frame, 'Card found!')
        if len(faces) == 1:
            face = faces[0]
            offset = 20
            x1 = face[0] - offset
            x2 = face[0] + face[2] + offset
            y1 = face[1] - offset
            y2 = face[1] + face[3] + offset
            crop = frame[y1:y2, x1:x2]
            cv2.imwrite("Cropped Image.jpg", crop)
    else:
        frame = writeText(frame, 'Scanning...')

    cv2.imshow('image', frame)
    if cv2.waitKey(1) == ord('q'):
        raise WindowsClosed


def runCamera(cam):
    # Original Source: https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html

    try:
        capture = cv2.VideoCapture(cam)
    except cv2.error:
        print("An Error has occurred")
        exit()

    if not capture.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = capture.read()

        if not ret:
            print("-- Stream ended --")
            break

        try:
            templatematching(frame, 'template')
        except WindowsClosed:
            break

    capture.release()
    cv2.destroyAllWindows()
