from abc import ABC, abstractmethod

import cv2

from finalisation.utils.Position import Position


class Detector(ABC):

    def __init__(self, id, frame, queue):
        super().__init__()
        self.id = id
        self.queue = queue
        self.frame = frame
        self.grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.template = 'truetemplate.jpg'
        self.facePosition = None

    @abstractmethod
    def isAcceptableStudentCard(self):
        pass

    @abstractmethod
    def retrieveData(self):
        pass

    def getQuality(self):
        return cv2.PSNR(self.grayFrame, cv2.equalizeHist(self.grayFrame))

    def isFaceCloseEnough(self):
        faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(self.frame, 1.1, 4)

        # Check for a face
        if len(faces) != 1:
            return False

        face = faces[0]

        # Check if face is close enough by length
        if face[2] <= 80 and face[3] <= 80:
            return False
        else:
            offset = 20
            x1 = face[0] - offset
            y1 = face[1] - offset
            x2 = face[0] + face[2] + offset
            y2 = face[1] + face[3] + offset
            self.facePosition = Position(x1, y1, x2, y2)
            return True

