import time
import numpy

from lib.data.students import Students
from lib.debugging import config
from lib.debugging.debugging import Debugging
from lib.debugging.subdirectory import Subdirectory
from lib.detector.detector import Detector
from lib.detector.hmldetector import HMLDetector
from lib.interfaces.mediator.component import Component
from lib.utils.exceptions import AddingStudentError, MaxSeatError
from lib.interfaces.thread.thread import Thread


class Processing(Thread, Debugging, Component):
    def __init__(self, students: Students):
        Thread.__init__(self)
        Debugging.__init__(self, Subdirectory.PROCESSING)
        self._buffer_size = -1
        self._main_buffer = list()
        self._students = students
        self.detection_option = 1
        self._target = config.get_config('project', 'show_target')
        self.capture_frame = None

    @property
    def target(self) -> bool:
        if self._target == "True":
            return True
        return False

    @property
    def buffer_size(self) -> int:
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size: int) -> None:
        self._buffer_size = buffer_size

    @buffer_size.deleter
    def buffer_size(self) -> None:
        self._buffer_size = -1

    @property
    def main_buffer(self) -> list:
        return self._main_buffer

    @main_buffer.deleter
    def main_buffer(self) -> None:
        self._main_buffer.clear()

    def is_active(self):
        return self.buffer_size != -1

    def is_main_buffer_full(self) -> bool:
        return len(self.main_buffer) >= self.buffer_size

    def _mainloop(self) -> None:
        while self.is_running():
            if self.is_active():
                if self.target is True:
                    if len(self.main_buffer) > 0:
                        self.capture_frame = self.get_detection(self.main_buffer[len(self.main_buffer)-1]).draw_rectangle()
                else:
                    time.sleep(0.1)
                if self.is_main_buffer_full():
                    detector = self.get_detection(self.main_buffer[0])
                    del self.main_buffer
            else:
                time.sleep(0.1)

    def get_detection(self, frame) -> Detector:
        if self.detection_option == 1:
            return HMLDetector(frame)

    # def _run(self) -> None:
    #     detectors = list()
    #     for i in range(10):
    #         detectors.append(self.get_detection(self.main_buffer[i]))
    #
    #     highest_quality = 0
    #     index = 0
    #     for i, v in enumerate(detectors):
    #         quality = v.get_quality()
    #         if quality > highest_quality:
    #             highest_quality = quality
    #             index = i
    #
    #     data = detectors[index].retrieve_data()
    #
    #     if data is None:
    #         self.mediator.set_response("Student Card could not be read")
    #         self.log("_run(): Data was None")
    #     else:
    #         try:
    #             self._students.students_list = data
    #             self.mediator.set_response(f"Student '{data['last_name']} {data['first_name']}' has been added")
    #         except AddingStudentError as error:
    #             self.log(f"_run(): {error}")
    #         except MaxSeatError:
    #             self.mediator.set_response(f"Must set Max seat first")

    def add_queue(self, e: numpy) -> None:
        if self.is_active():
            self.main_buffer.append(e)

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()
