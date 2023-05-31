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
    def check(self):
        pass

    def retrieve_data(self):
        pass

    template = "truetemplate.jpg"

    @property
    def card(self) -> Position:
        """
        Retrieves the location of the student card.

        This method returns the location of the student card, represented as a `Position` object.
        If the card location has not been determined yet, the method performs the necessary checks
        and calculations to determine the card's position based on the detected face.

        :return: The location of the student card as a `Position` object.
        :rtype: Position
        """
        if self._card is None:
            if self.is_card():
                face = self.face
                if face is not None:
                    x1 = face.x1 - round(face.get_width(3))
                    y1 = face.y1 - round(face.get_height(0.9))
                    x2 = face.x2 + round(face.get_width(1 / 2.5))
                    y2 = face.y2 + round(face.get_height(0.8))
                    self._card = Position(x1, y1, x2, y2)
                    return self._card

        return self._card

    def is_card(self) -> bool:
        return bool(self._check_template() and self._is_enough_features())

    def _check_template(self):
        """
        Checks if the template is acceptable or not.

        This method verifies the template by performing several checks:
        - It ensures that the template file extension is supported by OpenCV.
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

            print(len(goodMatches))
            return len(goodMatches)

        return 0

    def draw_rectangle(self) -> numpy:
        """
        Draws and returns a rectangle on the current image if a card is found.

        This method draws a rectangle on the current frame, indicating the location and size of the detected card.
        It also adds text displaying the width and height of the card within the rectangle.

        :returns: An array representation of the modified image.
        :rtype: numpy.ndarray

        """
        if self.card is not None:
            rectangle = cv2.rectangle(self.frame,
                                      (self.card.x1, self.card.y1),
                                      (self.card.x2, self.card.y2),
                                      (0, 0, 255),
                                      2)
            textx = cv2.putText(rectangle,
                                f"{self.card.get_width()} px",
                                (int(self.card.x1 + self.card.get_width() / 2 - 50), self.card.y1 - 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                2)
            texty = cv2.putText(textx,
                                f"{self.card.get_height()} px",
                                (int(self.card.x1 + 20), int(self.card.y1 + self.card.get_height() / 2)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255),
                                2)
            if self.is_debugging():
                cv2.imwrite('rectangle_frame_.jpg', texty)
            return texty
        else:
            return self.frame
