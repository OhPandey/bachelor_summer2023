from abc import ABC, abstractmethod

import cv2


class Detector(ABC):

    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.template = 'truetemplate.jpg'

    @abstractmethod
    def isStudentCard(self):
        pass

    def getQuality(self):
        sharpness = cv2.Laplacian(self.grayFrame, cv2.CV_64F).var()
        brightness = cv2.mean(self.grayFrame)[0]
        min_val, max_val, _, _ = cv2.minMaxLoc(self.grayFrame)
        contrast = (max_val - min_val) / max_val

        return sharpness+brightness+contrast
