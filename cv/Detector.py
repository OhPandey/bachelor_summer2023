from abc import ABC, abstractmethod

import cv2
import easyocr

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class WindowsClosed(Exception):
    pass


class Detector(ABC):

    IMAGE = 1
    CAPTURE = 2

    def __init__(self, value, type, state):

        self.currentNormalFrame = None
        self.currentGrayFrame = None
        self.facePosition = None
        self.cardPosition = None
        self.state = state

        if type == self.IMAGE:
            self.runImage(value)
        elif type == self.CAPTURE:
            self.runCapture()
        else:
            self.type = None
            print("Type is not supported")

    # Actual abstract method to be implemented.
    @abstractmethod
    def main(self):
        pass

    # Running as image
    def runImage(self, value):
        self.type = 1
        self.currentNormalFrame = cv2.imread(value)
        self.main()

    # Running as capture
    def runCapture(self):
        self.type = 2
        try:
            capture = cv2.VideoCapture(0)
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
                self.currentNormalFrame = frame
                self.cardPosition = None
                self.facePosition = None
                self.currentGrayFrame = cv2.cvtColor(self.currentNormalFrame, cv2.COLOR_BGR2GRAY)
                self.main()

                cv2.imshow('Stream', self.currentNormalFrame)
                cv2.imshow('Streamgray', self.currentGrayFrame)
                if self.type == self.IMAGE:
                    cv2.waitKey(0)

                if self.type == self.CAPTURE:
                    if cv2.waitKey(1) == ord('q'):
                        raise WindowsClosed

            except WindowsClosed:
                print("-- Stream manually ended --")
                break

        capture.release()
        cv2.destroyAllWindows()

    def _faceScan(self):

        faces = face_cascade.detectMultiScale(self.currentNormalFrame, 1.1, 4)

        # Check for a face
        if len(faces) == 1:
            face = faces[0]

            # Check if the face is close enough
            if face[2] >= 80 and face[3] >= 80:
                offset = 20
                x1 = face[0] - offset
                y1 = face[1] - offset
                x2 = face[0] + face[2] + offset
                y2 = face[1] + face[3] + offset
                cv2.imwrite("Cropped Image.jpg", self.currentNormalFrame[y1:y2, x1:x2])

                self.facePosition = Position(x1, y1, x2, y2)

                if self.state == 'development':
                    cv2.rectangle(self.currentNormalFrame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    def _textScan(self, frame):

        reader = easyocr.Reader(['en'], gpu=True)
        blur = cv2.GaussianBlur(frame, (5, 5), 1)
        result = reader.readtext(blur)
        for (bbox, text, prob) in result:
            if prob >= 0.5:
                print(f'Detected text: {text} (Probability: {prob:.2f})')

    def _isQualityGoodEnough(self, frame):
        SHARPNESS_THRESHOLD = 450
        BRIGHTNESS_THRESHOLD = 100

        sharpness = cv2.Laplacian(frame, cv2.CV_64F).var()
        brightness = cv2.mean(frame)[0]
        min_val, max_val, _, _ = cv2.minMaxLoc(frame)
        contrast = (max_val - min_val) / max_val

        print(f"sharpness: {sharpness}")
        print(f"brightness: {brightness}")
        print(f"contrast: {contrast}")
        if sharpness > SHARPNESS_THRESHOLD and brightness > BRIGHTNESS_THRESHOLD:
            return True
        else:
            return False
