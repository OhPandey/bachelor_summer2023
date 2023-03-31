import cv2
import numpy as np
import easyocr
from matplotlib import pyplot as plt

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class WindowsClosed(Exception):
    ...
    pass


def recognize_text(image):
    reader = easyocr.Reader(['en'], gpu=True)
    return reader.readtext(image)


def runScan(frame):
    facedata = faceScan(frame)
    if facedata is not None:
        # Facerectangle
        cv2.rectangle(frame, (facedata[0], facedata[1]), (facedata[2], facedata[3]), (0, 255, 255), 2)

        # Cardrectangle
        card = cardIt(facedata)
        cv2.rectangle(frame, (card[0], card[1]), (card[2], card[3]), (255, 255, 255), 2)


def cardIt(facedata):
    if facedata is not None:
        print(facedata[5])
        x1 = facedata[0] - round(facedata[4] * 2.75)
        y1 = facedata[1] - round(facedata[5] * 0.75)
        x2 = facedata[2] + round(facedata[4] / 2.5)
        y2 = facedata[3] + round(facedata[5] * 0.75)

        return [x1, y1, x2, y2]

    return None


def featurematching(frame):
    img1 = cv2.imread('truetemplate.jpg', 0)
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=1000)

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []

    for i, pair in enumerate(matches):
        try:
            m, n = pair
            if m.distance <= 0.72 * n.distance:
                good.append(m)
        except ValueError:
            pass

    # print(len(good))

    if len(good) >= 10:
        runScan(frame)
    else:
        frame = writeText(frame, '[Scanning...]')

    cv2.imshow('test', frame)
    if cv2.waitKey(1) == ord('q'):
        raise WindowsClosed


# def templatematching(frame):
#     img_bgr = frame
#     img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
#
#     template = cv2.imread('studentcard2.png', 0)
#     for size in range(50, 200):
#         width = int(template.shape[1] * size / 100)
#         height = int(template.shape[0] * size / 100)
#         resized = cv2.resize(template, (width, height), interpolation=cv2.INTER_AREA)
#         w, h = resized.shape[::-1]
#
#         res = cv2.matchTemplate(img_gray, resized, cv2.TM_CCOEFF_NORMED)
#         treshold = 0.7
#         loc = np.where(res >= treshold)
#
#         for pt in zip(*loc[::-1]):
#             cv2.rectangle(img_bgr, pt, (pt[0] - 10 + round((w * 0.8 * 2)), pt[1] + h * 4), (0, 255, 255), 2)
#
#     cv2.imshow('test', img_bgr)
#     if cv2.waitKey(1) == ord('q'):
#         raise WindowsClosed


# def featurematching(frame):
#     img = cv2.imread('photo.jpg', 0)
#
#     # recognize text
#     result = recognize_text('photo.jpg')
#
#     # if OCR prob is over 0.5, overlay bounding box and text
#     for (bbox, text, prob) in result:
#         if prob >= 0.7:
#             # display
#             print(f'Detected text: {text} (Probability: {prob:.2f})')
#
#             # get top-left and bottom-right bbox vertices
#             (top_left, top_right, bottom_right, bottom_left) = bbox
#             top_left = (int(top_left[0]), int(top_left[1]))
#             bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
#
#             # create a rectangle for bbox display
#             cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(255, 0, 0), thickness=1)
#
#             # put recognized text
#             cv2.putText(img=img, text=text, org=(top_left[0], top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                         fontScale=0.5, color=(255, 0, 0), thickness=1)
#
#     # show and save image
#     cv2.imshow('test', img)
#     cv2.waitKey(0)

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
            featurematching(frame)
        except WindowsClosed:
            break

    capture.release()
    cv2.destroyAllWindows()
