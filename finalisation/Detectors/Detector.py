from abc import ABC, abstractmethod

import cv2
from easyocr import easyocr
from finalisation.utils.State import State

# import easyocr

from finalisation.utils.Position import Position


class Detector(ABC):
    # Configuration
    face_size = 80
    face_offset = 20
    card_width = 1 / 2
    card_height = 1 / 2
    state = State.DEVELOPMENT

    # No Configuration
    quality = None
    gray_frame = None
    face = None
    card = None

    def __init__(self, frame, queue=None):
        self.queue = queue
        self.frame = frame
        self.face_position = None
        self.card_position = None
        self.data = None

    @abstractmethod
    def check(self):
        pass

    # Image Functions
    def get_colored_frame(self):
        return self.frame

    def get_grayed_frame(self):
        if self.gray_frame is None:
            self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        return self.gray_frame

    def get_quality(self):
        if self.quality is None:
            self.quality = cv2.PSNR(self.get_grayed_frame(), cv2.equalizeHist(self.get_grayed_frame()))

        return self.quality

    # Face Functions
    def get_face(self):
        if self.face is None:
            faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(self.frame, 1.1, 4)

            if len(faces) != 1:
                return None

            face = faces[0]

            x1 = face[0]
            y1 = face[1]
            x2 = face[0] + face[2]
            y2 = face[1] + face[3]

            self.face = Position(x1, y1, x2, y2)

        return self.face

    def adjust_face(self):
        if self.face is not None:
            if self.face.adjusted is False:
                self.face.add_offset(self.face_offset)

    # Card Functions
    def card_check(self):

        if self.card is None:
            return False

        if not isinstance(self.card, Position):
            return False

        if self.card.x1 < 0 or self.card.y2 < 0:
            return False

        h, w, z = self.frame.shape

        if self.card.x2 > w or self.card.y2 > h:
            return False

        if self.card.get_width() < w * self.card_width or self.card.get_height() < h * self.card_height:
            return False

        return True
