import time

import numpy

from lib.data.students import Students
from lib.detectors.detector import Detector
from lib.detectors.hmldetector import HMLDetector
from lib.utils.exceptions import AddingStudentError
from lib.utils.threading import Threading


class Processing(Threading):
    def __init__(self, students: Students, fps: int):
        super().__init__()
        self.buffer_size = fps
        self.main_buffer = list()
        self.students = students
        self.detection_option = 1

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()

    def is_main_buffer_full(self) -> bool:
        return len(self.main_buffer) >= self.buffer_size

    def flush(self) -> None:
        self.main_buffer.clear()

    def _mainloop(self) -> None:
        while self.is_running():
            if self.is_main_buffer_full():
                detector = self.get_detection(self.main_buffer[0])
                if detector.check() == 2:
                    self._run()
                self.flush()
            else:
                time.sleep(0.1)

    def get_detection(self, frame) -> Detector:
        if self.detection_option == 1:
            return HMLDetector(frame)

    def _run(self) -> None:
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

    def add_queue(self, e: numpy) -> None:
        self.main_buffer.append(e)
