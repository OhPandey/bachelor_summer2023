import configparser
import os

import cv2
import numpy
from PIL import Image

from lib.debugging.debugging import Debugging
from lib.detector.detector import Detector
from lib.data.dataset import OPENCV_SUPPORTED_IMREAD_FORMATS
from lib.utils.position import Position


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector, Debugging):

    template = "truetemplate.jpg"

    @property
    def card(self) -> Position:
        """
        Getter method for the card position

        This method returns the location of the student card, represented as a `Position` object.
        If the card location has not been determined yet, the method performs the necessary checks
        and calculations to determine the card's position based on the detected face.

        :return: The location of the student card
        :rtype: Position
        """
        if self._card is None:
            if self.is_card():
                face = self.face
                if face is not None:
                    x1 = face.x1 - round(face.get_width(4.25))
                    y1 = face.y1 - round(face.get_height(1.5))
                    x2 = face.x2 + round(face.get_width(0.5))
                    y2 = face.y2 + round(face.get_height(1.25))
                    self._card = Position(x1, y1, x2, y2)
                    return self._card

        return self._card

    def is_card(self) -> bool:
        return bool(self._is_template() and self._is_enough_features())

    def _is_template(self):
        """
        Checks if the template is acceptable or not.

        This method verifies the template by performing several checks:
        - It ensures that the template file extension is supported by OpenCV's formats.
        - It checks if the template file exists.
        - It attempts to open the template image using the Pillow library and verifies its integrity.

        :return: A boolean value indicating whether the template is acceptable.
                 Returns True if the template meets the criteria, and False otherwise.
        :rtype: bool
        """

        if not self.template.endswith(tuple(OPENCV_SUPPORTED_IMREAD_FORMATS)):
            return False

        if not os.path.isfile(self.template):
            return False
        try:
            img = Image.open(self.template)
            img.verify()
            img.close()
            return True
        except (OSError, IOError, Image.DecompressionBombError, SyntaxError, ValueError):
            return False

    def _is_enough_features(self):
        """
        Determines if there are enough features using the feature matching approach

        This method checks if there are enough features found based the private function find_features()

        :return: A boolean value indicating whether there are enough features.
                 Returns True if there are enough features, and False otherwise.
        :rtype: bool
        """
        return bool(self._find_features() >= 10)

    def _find_features(self) -> int:
        """
        Finds and returns the number of features based on the template image.

        This method uses the SIFT algorithm to detect and compute features in the template image
        and the current frame being processed. It then performs feature matching using the BFMatcher.

        :return: The number of good matches found.
        :rtype: int
        """
        template = cv2.imread(self.template, 0)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(self.gray_frame, None)

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