import time

from lib.data.students import Students
from lib.detectors.hmldetector import HMLDetector
from lib.utils.exceptions import AddingStudentError
from lib.utils.threading import Threading


class Processing(Threading):
    def __init__(self, students: Students):
        super().__init__()
        self.fps = None
        self.buffer_size = 10
        self.main_buffer = list()
        self.overflow_buffer = list()
        self.students = students
        self.detection_option = 1

    def start(self):
        super().start()

    def set_fps(self, value):
        self.fps = value

    def stop(self):
        super().stop()

    def is_mainbufferfull(self):
        return len(self.main_buffer) >= self.buffer_size

    def is_overflowbufferfull(self):
        return len(self.overflow_buffer) >= self.buffer_size

    def flush(self):
        self.main_buffer.clear()
        self.main_buffer = self.overflow_buffer[-10:]
        # if len(self.overflowbuffer) >= 10:
        #    print(f"Frames dropped:{len(self.overflowbuffer) - 10}")
        self.overflow_buffer.clear()

    def _mainloop(self):
        while self._running:
            if self.is_mainbufferfull():
                detector = self.get_detection(self.main_buffer[0])
                if detector.check() == 2:
                    self._run()
                self.flush()
            else:
                time.sleep(0.1)

    def get_detection(self, frame):
        if self.detection_option == 1:
            return HMLDetector(frame)

    def _run(self):
        detectors = list()
        for i in range(10):
            detectors.append(self.get_detection(self.main_buffer[i]))

        highest_quality = 0
        index = 0
        for i, v in enumerate(detectors):
            quality = v.get_quality()
            if quality > highest_quality:
                highest_quality = quality
                index = i

        data = detectors[index].retrieve_data()
        if data is None:
            print("Impossible to read the data.")
        else:
            try:
                print(data)
                self.students.add_student(data)
            except AddingStudentError as error:
                print(error)

    def add_queue(self, e):
        if not self.is_mainbufferfull():
            self.main_buffer.append(e)
        else:
            self.overflow_buffer.append(e)
