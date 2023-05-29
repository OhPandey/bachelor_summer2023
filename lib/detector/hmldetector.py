import configparser
import os

import cv2
from PIL import Image

from lib.debugging.debugging import Debugging
from lib.detector.detector import Detector
from lib.data.dataset import OPENCV_SUPPORTED_IMREAD_FORMATS
from lib.utils.position import Position

config = configparser.ConfigParser()
config.read('config.ini')


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector, Debugging):
    template = "test.jpg"

    def check(self):
        if not self.is_template_legal():
            return 3

        if self._find_features() < 10:
            return 2

        self.get_face()
        self.card = self._transform_face_into_card()

        if self.card_check() is False:
            return 1

        return 0

    def retrieve_data(self):
        self.get_face()
        self.card = self._transform_face_into_card()
        return super().retrieve_data()

    def is_template_legal(self):
        if not self.template.endswith(tuple(OPENCV_SUPPORTED_IMREAD_FORMATS)):
            return False

        project_root = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(project_root, self.template)

        if not os.path.isfile(template_path):
            return False

        try:
            img = Image.open(template_path)
            img.verify()
            img.close()
            return True
        except Exception:
            return False

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
        x2 = self.face.x2 + round(self.face.get_width(1 / 2.5))
        y2 = self.face.y2 + round(self.face.get_height(0.8))

        return Position(x1, y1, x2, y2)
