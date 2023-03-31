from abc import ABC, abstractmethod

import cv2

from cv.Position import Position

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class WindowsClosed(Exception):
    pass


class Detector(ABC):
    facePosition = None
    cardPosition = None
    currentFrame = None
    runningOn = None

    state = 'debugging'

    @abstractmethod
    def runImage(self, image):
        self.runningOn = 'image'
        self.currentFrame = cv2.imread(image)
        self.main()

    @abstractmethod
    def runCapture(self, cap):
        self.runningOn = 'video'
        try:
            capture = cv2.VideoCapture(cap)
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
                self.currentFrame = frame
                self.main()
            except WindowsClosed as e:
                print("-- Stream ended --")
                break

        capture.release()
        cv2.destroyAllWindows()

    @abstractmethod
    def main(self):
        pass

    def faceScan(self):
        faces = face_cascade.detectMultiScale(self.currentFrame, 1.1, 4)

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
                w = x2 - x1
                h = y2 - y1
                cv2.imwrite("Cropped Image.jpg", self.currentFrame[y1:y2, x1:x2])

                self.facePosition = Position(x1, y1, x2, y2)

                if self.state == 'debugging':
                    cv2.rectangle(self.currentFrame, (x1, y1), (x2, y2), (0, 255, 255), 2)
