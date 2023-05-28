import time
import numpy

from lib.data.students import Students
from lib.debugging.debugging import Debugging
from lib.debugging.subdirectory import Subdirectory
from lib.detectors.detector import Detector
from lib.detectors.hmldetector import HMLDetector
from lib.mediator.component import Component
from lib.utils.exceptions import AddingStudentError
from lib.utils.threads import Threading


class Processing(Threading, Debugging, Component):
    def __init__(self, students: Students):
        Threading.__init__(self)
        Debugging.__init__(self, Subdirectory.PROCESSING)
        self._buffer_size = -1
        self._main_buffer = list()
        self._students = students
        self.detection_option = 1

    @property
    def buffer_size(self) -> int:
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size: int) -> None:
        self._buffer_size = buffer_size

    @buffer_size.deleter
    def buffer_size(self):
        self._buffer_size = -1

    @property
    def main_buffer(self):
        return self._main_buffer

    @main_buffer.deleter
    def main_buffer(self):
        self._main_buffer.clear()

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()

    def is_active(self):
        return self.buffer_size != -1

    def is_main_buffer_full(self) -> bool:
        return len(self._main_buffer) >= self.buffer_size

    def _mainloop(self) -> None:
        while self.is_running():
            if self.is_active():
                if self.is_main_buffer_full():
                    self.mediator.update('1')
                    detector = self.get_detection(self._main_buffer[0])
                    if detector.check() == 2:
                        self._run()

                    del self._main_buffer
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

    def get_detection(self, frame) -> Detector:
        if self.detection_option == 1:
            return HMLDetector(frame)

    def _run(self) -> None:
        detectors = list()
        for i in range(10):
            detectors.append(self.get_detection(self._main_buffer[i]))

        highest_quality = 0
        index = 0
        for i, v in enumerate(detectors):
            quality = v.get_quality()
            if quality > highest_quality:
                highest_quality = quality
                index = i

        data = detectors[index].retrieve_data()
        if data is None:
            self.log("Data could not be read")
        else:
            try:
                print(data)
                self._students.add_student(data)
            except AddingStudentError as error:
                print(error)

    def add_queue(self, e: numpy) -> None:
        if self.is_active():
            self._main_buffer.append(e)
