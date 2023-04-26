import cv2

from cv.Detector import Detector, WindowsClosed
from cv.RectanglePosition import Position


# Non-Machine Learning Approach
class NMLDetectorOne(Detector):
    template = 'truetemplate.jpg'

    def main(self):
        if self.currentNormalFrame is None:
            raise WindowsClosed

        # Get Template
        template = cv2.imread(self.template, 0)
        # Feature matching with orb
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(self.currentGrayFrame, None)
        if des2 is not None:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            if self._findAmountOfGoodMatches(matches) >= 10:
                super()._faceScan()

                if self.facePosition is not None:
                    self._positionCardOutOfFace()

                if self.cardPosition is not None:
                    if super()._isQualityGoodEnough(self.currentGrayFrame):
                        card = self.currentGrayFrame[self.cardPosition.getY1():self.cardPosition.getY2(),
                               self.cardPosition.getX1():self.cardPosition.getX2()]
                        cv2.imwrite('Cropped Card.jpg', card)
                        super()._textScan(card)
            else:
                pass

    def _findAmountOfGoodMatches(self, matches):
        goodMatches = []

        for i, pair in enumerate(matches):
            try:
                m, n = pair
                if m.distance <= 0.5 * n.distance:
                    goodMatches.append(m)
            except ValueError:
                pass
        print(len(goodMatches))
        return len(goodMatches)

    def _positionCardOutOfFace(self):
        if self.facePosition is not None:
            x1 = self.facePosition.getX1() - round(self.facePosition.getWidth() * 2.9)
            y1 = self.facePosition.getY1() - round(self.facePosition.getHeight() * 0.9)
            x2 = self.facePosition.getX2() + round(self.facePosition.getWidth() / 2.5)
            y2 = self.facePosition.getY2() + round(self.facePosition.getHeight() * 0.75)
            self.cardPosition = Position(x1, y1, x2, y2)

            if self.state == 'development':
                cv2.rectangle(self.currentNormalFrame, (x1, y1), (x2, y2), (255, 255, 255), 2)
