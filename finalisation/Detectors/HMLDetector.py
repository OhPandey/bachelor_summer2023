import cv2

from finalisation.Detectors.Detector import Detector
from finalisation.utils.Position import Position


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector):
    def isAcceptableStudentCard(self):
        if self._findFeatures() >= 10:
            if self.isFaceCloseEnough():
                print('I found an acceptable Student Card!')
                return True

        return False

    def _findFeatures(self):
        template = cv2.imread(self.template, 0)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(self.grayFrame, None)

        if des2 is not None:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            goodMatches = []

            for i, pair in enumerate(matches):
                try:
                    m, n = pair
                    if m.distance <= 0.5 * n.distance:
                        goodMatches.append(m)
                except ValueError:
                    pass
            return len(goodMatches)

        return 0

    def retrieveData(self):
        pass

    def printFrameWithText(self):
        cv2.putText(self.frame, str(self.getQuality()), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
        cv2.imwrite('debugging/image' + str(self.id) + '.jpg', self.frame)
        return self.queue.put((self.id, self.getQuality()))
