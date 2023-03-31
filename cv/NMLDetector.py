import cv2

from cv.Detector import Detector, WindowsClosed
from cv.Position import Position


# Non-Machine learning Detector
class NMLDetector(Detector):
    template = 'truetemplate.jpg'

    def runImage(self, image):
        super().runImage(image)

    def runCapture(self, cap):
        super().runCapture(cap)

    def main(self):
        if self.currentFrame is None:
            raise WindowsClosed

        img1 = cv2.imread(self.template, 0)

        img2 = cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create(nfeatures=1000)

        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        if self.findAmountOfGoodMatches(matches) >= 10:
            self.faceScan()

            if self.facePosition is not None:
                self.positionCardOutOfFace()

        else:
            pass

        cv2.imshow('test', self.currentFrame)

        if self.state == 'debugging' and self.runningOn == 'image':
            cv2.waitKey(0)

        if self.state == 'debugging' and self.runningOn == 'video':
            if cv2.waitKey(1) == ord('q'):
                raise WindowsClosed

    def findAmountOfGoodMatches(self, matches):
        goodMatches = []

        for i, pair in enumerate(matches):
            try:
                m, n = pair
                if m.distance <= 0.72 * n.distance:
                    goodMatches.append(m)
            except ValueError:
                pass

        if self.state == 'debugging':
            print(len(goodMatches))
        return len(goodMatches)

    def positionCardOutOfFace(self):
        if self.facePosition is not None:
            x1 = self.facePosition.getX1() - round(self.facePosition.getWidth() * 2.75)
            y1 = self.facePosition.getY1() - round(self.facePosition.getHeight() * 0.75)
            x2 = self.facePosition.getX2() + round(self.facePosition.getWidth() / 2.5)
            y2 = self.facePosition.getY2() + round(self.facePosition.getHeight() * 0.75)
            self.cardPosition = Position(x1, y1, x2, y2)

            if self.state == 'debugging':
                cv2.rectangle(self.currentFrame, (x1, y1), (x2, y2), (255, 255, 255), 2)
