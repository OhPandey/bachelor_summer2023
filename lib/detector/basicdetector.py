import configparser
import os

import cv2
import numpy as np
from PIL import Image

from lib.debugging.debugging import Debugging
from lib.detector.detector import Detector
from lib.data.dataset import OPENCV_SUPPORTED_IMREAD_FORMATS
from lib.utils.position import Position


class BasicDetector(Detector, Debugging):
    template = "truetemplate.jpg"

    @property
    def card(self) -> Position | None:
        """
        Getter method for the card position

        This method returns the location of the student card, represented as a `Position` object.
        If the card location has not been determined yet, the method performs the necessary checks
        and calculations to determine the card's position based on the detected face.

        :return: The location of the student card
        :rtype: Position
        """
        if self._card is None:
            if self._is_card():
                self._card = self.potential_position
                return self._card

        return self._card

    def _is_card(self) -> bool:
        if not self._is_template():
            return False

        return self._is_feature_matching()

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

    def _is_feature_matching(self) -> bool:
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

            good_matches = []

            for i, pair in enumerate(matches):
                try:
                    m, n = pair
                    if m.distance <= 0.5 * n.distance:
                        good_matches.append(m)
                except ValueError:
                    pass

            if len(good_matches) >= 10:
                try:
                    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                    h, w = template.shape
                    corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    transformed_corners = cv2.perspectiveTransform(corners, M)

                    x_coordinates = [coord[0][0] for coord in transformed_corners]
                    y_coordinates = [coord[0][1] for coord in transformed_corners]
                    x1, x2 = min(x_coordinates), max(x_coordinates)
                    y1, y2 = min(y_coordinates), max(y_coordinates)

                    self.potential_position = Position(int(x1), int(y1), int(x2), int(y2))
                except Exception:
                    return False
                return True

        return False
