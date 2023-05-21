import cv2

from finalisation.Detectors.detector import Detector
from finalisation.utils.position import Position
from finalisation.utils.state import State


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector):
    template = 'truetemplate.jpg'

    def check(self):
        if self._find_features() < 10:
            return 0

        self.get_face()
        self.card = self._transform_face_into_card()

        if self.card_check() is False:
            return 1

        self.retrieve_data()

        return 2

    def _find_features(self) -> int:
        template = cv2.imread(self.template, 0)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(self.get_grayed_frame(), None)

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

                if self.state == State.DEBUGGING:
                    print(len(goodMatches))

            return len(goodMatches)

        return 0

    def _transform_face_into_card(self) -> Position | None:
        if self.face is None:
            return None

        if not isinstance(self.face, Position):
            return None

        x1 = self.face.x1 - round(self.face.get_width(3))
        y1 = self.face.y1 - round(self.face.get_height(0.9))
        x2 = self.face.x2 + round(self.face.get_width(1/2.5))
        y2 = self.face.y2 + round(self.face.get_height(0.8))

        return Position(x1, y1, x2, y2)
