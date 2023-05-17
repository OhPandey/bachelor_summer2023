import cv2

from finalisation.Detectors.Detector import Detector
from finalisation.utils.Position import Position


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector):
    def is_acceptable_student_card(self):
        if self._find_features() >= 10:
            print('Its something')
            if self.is_face_close_enough():
                print('Face is ok')
                if self.is_card_close_enough():
                    print('I found an acceptable Student Card!')
                return True

        return False

    def _find_features(self):
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
                # print(len(goodMatches))
            return len(goodMatches)

        return 0

    def retrieveData(self):
        pass

    def is_face_close_enough(self):
        face = self.get_face()
        if self.get_face() is None:
            return False

        # Check if face is close enough (by pixel length of face_size)
        if face[2] >= self.face_offset and face[3] >= self.face_offset:
            self.face_position = self._get_face_position(face)
            self.transform_face_into_card()
            return True
        else:
            return False

    # This is function which transforms the position of the face into a student card.
    # It is hard-coded and only works for the specific student cards.
    def transform_face_into_card(self):
        if self.face_position is None:
            return None

        if not isinstance(self.face_position, Position):
            return None

        x1 = self.face_position.get_x1() - round(self.face_position.get_width() * 2.9)
        y1 = self.face_position.get_y1() - round(self.face_position.get_height() * 0.9)
        x2 = self.face_position.get_x2() + round(self.face_position.get_width() / 2.5)
        y2 = self.face_position.get_y2() + round(self.face_position.get_height() * 0.75)
        self.card_position = Position(x1, y1, x2, y2)
