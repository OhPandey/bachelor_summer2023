from abc import ABC, abstractmethod

import cv2
# import easyocr

from finalisation.utils.Position import Position


class Detector(ABC):
    face_size = 80
    face_offset = 20
    card_width = 300
    card_height = 200

    def __init__(self, frame, queue=None):
        super().__init__()
        self.queue = queue
        self.frame = frame
        self.grayFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.template = 'truetemplate.jpg'
        self.face_position = None
        self.card_position = None
        self.data = None

    @abstractmethod
    def is_acceptable_student_card(self):
        pass

    def retrieve_data(self):
        data = self.run_text_detection()

        if len(data) != 3:
            return None

        name = data[0]
        date = data[1]
        student_id = data[2]

        if len(name.split()) < 2:
            return None

        if len(date.split()) != 3:
            return None

        if len(student_id) != 10:
            return None

        return data

    def get_quality(self):
        return cv2.PSNR(self.grayFrame, cv2.equalizeHist(self.grayFrame))

    def queue_quality(self, id):
        cv2.putText(self.frame, str(self.get_quality()), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)
        cv2.imwrite('debugging/image' + str(id) + '.jpg', self.frame)
        return self.queue.put((id, self.get_quality()))

    def get_faces(self):
        return cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(self.frame, 1.1, 4)

    def get_face(self):
        face = self.get_faces()
        if len(self.get_faces()) != 1:
            return None

        return face[0]

    def is_card_close_enough(self):
        if self.card_position is None:
            return False
        if not isinstance(self.card_position, Position):
            return False
        h, w, z = self.frame.shape
        if self.card_position.get_x1() < 0 or self.card_position.get_y1() < 0:
            return False
        if self.card_position.get_x2() > w or self.card_position.get_y2() > h:
            return False
        if self.card_position.get_width() < self.card_width and self.card_position.get_height() < self.card_height:
            return False

        return True

    def _get_face_position(self, face):
        x1 = face[0] - self.face_offset
        y1 = face[1] - self.face_offset
        x2 = face[0] + face[2] + self.face_offset
        y2 = face[1] + face[3] + self.face_offset
        return Position(x1, y1, x2, y2)

    def run_text_detection(self):
        # reader = easyocr.Reader(['en'], gpu=True)
        # blur = cv2.GaussianBlur(self.frame, (5, 5), 1)
        # result = reader.readtext(blur)
        # for (bbox, text, prob) in result:
        #    if prob >= 0.5:
        #        print(f'Detected text: {text} (Probability: {prob:.2f})')

        # this is a mockup until I have the easyocr code finalised
        array = ['Da Silva Joey', '03 May 1997', '0181039342']

        return array
