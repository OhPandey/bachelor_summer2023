from abc import ABC, abstractmethod
import cv2
import numpy
from easyocr import easyocr
import pytesseract

from lib.debugging.config import get_config
from lib.utils.position import Position
from lib.utils.processing_data import processing_data_easyocr, processing_data_tesseract


class Detector(ABC):
    # Configuration
    face_size = 80
    face_offset = 20
    card_width = 0.5
    card_height = 0.5

    def __init__(self, frame):
        self._frame = frame
        self._gray_frame = None
        self._quality = None
        self._face = None
        self._card = None
        self.ocr = 2

    # Image Functions
    @property
    def frame(self) -> numpy:
        """
        Getter method for the (current) frame.

        :return: Frame
        :rtype: numpy.ndarray
        """
        return self._frame

    @property
    def gray_frame(self) -> numpy:
        """
        Getter method for the gray frame.

        In order to avoid multiple calculations, this method returns the gray frame.

        :return: Gray frame
        :rtype: numpy.ndarray
        """
        if self._gray_frame is None:
            self._gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        return self._gray_frame

    @property
    def quality(self) -> float:
        """
        Getter method for the quality of an image

        :return: The quality of an image
        :rtype: float
        """
        if self._quality is None:
            self._quality = cv2.PSNR(self.gray_frame, cv2.equalizeHist(self.gray_frame))

        return self._quality

    # Face Functions
    @property
    def face(self) -> Position | None:
        """
        Getter method for the face.

        If there is only one face detected, the position of the detected face is returned as a `Position` object.

        :return: The position of the (detected) face (or None)
        :rtype: Position | None
        """
        if self._face is None:
            faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(self.frame, 1.1, 4)

            if len(faces) == 1:
                face = faces[0]

                x1 = face[0]
                y1 = face[1]
                x2 = face[0] + face[2]
                y2 = face[1] + face[3]

                self._face = Position(x1, y1, x2, y2)

        return self._face

    # Card Function
    @abstractmethod
    def card(self) -> Position:
        """
        Returns the location of the student card.

        :return: The location of the student card
        :rtype: Position
        """
        pass

    def _is_card_outside_of_frame(self):
        """
        Checks if the card is outside the frame boundaries.

        :return: True if the card is outside the frame, False otherwise.
        :rtype: bool
        """
        h, w, z = self.frame.shape
        return bool(self.card().x1 < 0 or self.card().y2 < 0 or self.card().x2 > w or self.card().y2 > h)

    def _is_card_too_far(self):
        """
        Checks if the card is positioned too far from the expected configured size.

        :return: True if the card is too far from the expected configured size, False otherwise.
        :rtype: bool
        """
        h, w, z = self.frame.shape
        return bool(self.card().get_width() < w * self.card_width or self._card.get_height() < h * self.card_height)

    def card_check(self) -> int:
        """
        Performs a series of checks on the student card to determine its validity.

        :return: An integer indicating the result of the card check.
            - 0: The card passes all checks and is valid (for further process)
            - 1: The card is positioned too far from the expected configured size.
            - 2: The card is outside the frame boundaries.
            - 3: No card detected. (Should never occur)
        :rtype: int
        """
        if self.card() is None:
            return 3

        if self._is_card_outside_of_frame():
            return 2

        if self._is_card_too_far():
            return 1

        return 0

    @abstractmethod
    def is_card(self):
        """
        Determines whether the current frame has a student card or not.

        :return: A boolean value indicating whether the frame has a student card or not
                 Returns True if it meets the criteria of a card, and False otherwise.
        :rtype: bool
        """
        pass

    # Text-detection Functions
    def retrieve_data(self):
        if self.card is None:
            return None
        return self._text_detection()

    def _scanning_area(self) -> Position | None:
        """
        Gives the position of the area that is going to be scanned

        In order to reduce processing power, this method returns the Position where the OCR should happen.

        :return: The position of the scanning area on the card. Returns none if card doesn't exist.
        :rtype: Position | None
        """

        y1 = self.card.y1 + self.card.get_height(1 / 1.7)
        x2 = self.card.x2 - self.card.get_width(1 / 2.5)

        return Position(self.card.x1, y1, x2, self.card.y2)

    def _text_detection(self):
        area = self._scanning_area()
        frame = self.gray_frame[area.y1:area.y2, area.x1:area.x2]
        blur = cv2.GaussianBlur(frame, (5, 5), 1)

        # Debugging:
        # cv2.imwrite('debugging/realtest.jpg', blur)

        if self.ocr == 1:
            reader = easyocr.Reader(['en'], gpu=True)
            all_results = reader.readtext(blur)
            if all_results is None:
                return None

            results = list()

            for place, text, prob in all_results:
                if prob >= 0.5:
                    # Debugging
                    print(f'Detected text: {text}, {prob:.2f}')
                    results.append(text)

            if len(results) < 3:
                return None

            return processing_data_easyocr(results)

        if self.ocr == 2:
            pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
            result = pytesseract.image_to_data(blur,output_type=pytesseract.Output.DICT)

            results = list()

            for i, text in enumerate(result['text']):
                prob = int(result['conf'][i])
                if prob >= 90:
                    # Debugging
                    print(f"Word: {text}, Confidence: {prob}")
                    results.append(text)

            if len(results) < 3:
                return None
            print(results)
            return processing_data_tesseract(results)

        return None

    # Debugging
    def draw_rectangle(self) -> numpy:
        """
        Draws and returns a rectangle on the current image if a card is found.

        This method draws a rectangle on the current frame, indicating the location and size of the detected card.
        It also adds text displaying the width and height of the card within the rectangle.

        :returns: An array representation of the modified image.
        :rtype: numpy.ndarray

        """
        if self.card is not None:
            # Face
            face = cv2.rectangle(self.frame,
                                 (self.face.x1, self.face.y1),
                                 (self.face.x2, self.face.y2),
                                 (255, 0, 0),
                                 2)

            # Student card
            card = cv2.rectangle(face,
                                 (self.card.x1, self.card.y1),
                                 (self.card.x2, self.card.y2),
                                 (0, 0, 255),
                                 2)
            card_textx = cv2.putText(card,
                                     f"{self.card.get_width()} px",
                                     (int(self.card.x1 + self.card.get_width() / 2 - 50), self.card.y1 - 20),
                                     cv2.FONT_HERSHEY_SIMPLEX,
                                     1,
                                     (0, 0, 255),
                                     2)
            card_texty = cv2.putText(card_textx,
                                     f"{self.card.get_height()} px",
                                     (int(self.card.x1 + 10), int(self.card.y1 + self.card.get_height() / 2)),
                                     cv2.FONT_HERSHEY_SIMPLEX,
                                     1,
                                     (0, 0, 255),
                                     2)

            # Scanning area
            scan_position = self._scanning_area()
            scan = cv2.rectangle(card_texty,
                                 (scan_position.x1, scan_position.y1),
                                 (scan_position.x2, scan_position.y2),
                                 (0, 255, 0),
                                 2)

            scan_textx = cv2.putText(scan,
                                     f"{scan_position.get_width()} px",
                                     (
                                     int(scan_position.x1 + scan_position.get_width() / 2 - 50), scan_position.y1 + 30),
                                     cv2.FONT_HERSHEY_SIMPLEX,
                                     1,
                                     (0, 255, 0),
                                     2)
            scan_texty = cv2.putText(scan_textx,
                                     f"{scan_position.get_height()} px",
                                     (int(scan_position.x1 + 10),
                                      int(scan_position.y1 + scan_position.get_height() / 2)),
                                     cv2.FONT_HERSHEY_SIMPLEX,
                                     1,
                                     (0, 255, 0),
                                     2)

            return scan_texty
        else:
            return self.frame
