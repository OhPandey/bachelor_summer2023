from abc import ABC, abstractmethod
import re
import cv2
from easyocr import easyocr

from lib.debugging.config import get_config
from lib.utils.position import Position


class Detector(ABC):
    # Configuration
    face_size = 80
    face_offset = 20
    card_width = 0.5
    card_height = 0.5
    def __init__(self, frame):
        self.frame = frame
        self.quality = None
        self.frame = None
        self.gray_frame = None
        self.face = None
        self.card = None

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
    def get_face(self) -> Position | None:
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

            if self.face.adjusted is False:
                self.face.add_offset(self.face_offset)

        return self.face

    # Card Functions
    def card_check(self) -> bool:
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

    # Text-detection Functions
    @abstractmethod
    def retrieve_data(self):
        data = self._text_detection()
        return data

    def minimised_area(self) -> Position | None:
        if self.card is None:
            return None

        y1 = self.card.y1 + self.card.get_height(1 / 1.7)
        x2 = self.card.x2 - self.card.get_width(1 / 2.5)

        return Position(self.card.x1, y1, x2, self.card.y2)

    def _text_detection(self):
        area = self.minimised_area()

        if area is None:
            return None

        reader = easyocr.Reader(['en'], gpu=True)
        frame = self.get_grayed_frame()[area.y1:area.y2, area.x1:area.x2]
        blur = cv2.GaussianBlur(frame, (5, 5), 1)
        cv2.imwrite('debugging/realtest.jpg', blur)
        all_results = reader.readtext(blur)

        return self._process_data(all_results)

    def _process_data(self, all_results):
        # Evaluating the data
        if all_results is None:
            return None

        potential_results = list()
        for (place, text, prob) in all_results:
            print(f'Detected text: {text}, {prob:.2f}')
            if prob >= 0.5:
                potential_results.append(text)

        if len(potential_results) < 3:
            return None

        last_name = ""
        first_name = ""
        birth_day = None
        birth_year = None
        birth_month = None
        student_id = None

        for e in potential_results:
            if e.isnumeric() and len(e) == 10:
                student_id = e

        if student_id is not None:
            potential_results.remove(student_id)

        def is_year(value):
            return value.isnumeric() and len(value) == 4

        def is_month(value):
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
            pattern = r'^(?:' + '|'.join(months) + r')$'
            return bool(re.match(pattern, value, re.IGNORECASE))

        def is_day(value):
            return value.isnumeric() and len(value) == 2

        values = list()

        for e in potential_results:
            v = e.split()
            if len(v) >= 2:
                if v[0].isnumeric() or v[1].isnumeric():
                    found = list()
                    for p in v:
                        if is_year(p):
                            birth_year = p
                            found.append(birth_year)
                        if is_day(p):
                            birth_day = p
                            found.append(birth_day)
                    for q in found:
                        v.remove(q)

                    if is_month(v[0]):
                        birth_month = v[0]

                    values.append(e)

            if is_year(e) and birth_year is None:
                birth_year = e
                values.append(e)

            if is_day(e) and birth_day is None:
                birth_day = e
                values.append(e)

            if is_month(e) and birth_month is None:
                birth_month = e
                values.append(e)

        if len(values) >= 1:
            for e in values:
                potential_results.remove(e)

        for e in potential_results:
            v = e.split()
            for p in v:
                if p.isupper():
                    last_name += " " + p
                else:
                    first_name += " " + p

        if last_name != "":
            last_name = last_name[1:]

        if first_name != "":
            first_name = first_name[1:]

        return {
            'last_name': last_name,
            'first_name': first_name,
            'birth_day': birth_day,
            'birth_month': birth_month,
            'birth_year': birth_year,
            'student_id': student_id
        }
