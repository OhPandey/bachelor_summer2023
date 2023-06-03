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
        """
        Constructor.

        :param students: Instance of the Students class.
        :type students: Students
        """
        Thread.__init__(self)
        Debugging.__init__(self, Subdirectory.PROCESSING)
        self.log("__init__(): Started")
        self._buffer_size = -1
        self._main_buffer = list()
        self._students = students
        self.detection_option = 1
        self.capture_frame = None
        self.dropped_frames = 0

    @property
    def target(self) -> bool:
        """
        Get the target property from the configuration.

        This property determines whether the card is drawn or not. Careful: It takes a lot of processing power.

        :return: True if the target is enabled, False otherwise.
        :rtype: bool
         """
        if config.get_config('project', 'show_target') == "True":
            return True
        return False

    @property
    def buffer_size(self) -> int:
        """
        Get the buffer size.

        :return: The buffer size.
        :rtype: int
        """
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, buffer_size: int) -> None:
        """
        Set the buffer size.

        :param buffer_size: The buffer size to set.
        :type buffer_size: int
        """
        self._buffer_size = buffer_size
        self.log(f"buffer_size.setter: Buffer_size has been set to {buffer_size}")

    @buffer_size.deleter
    def buffer_size(self) -> None:
        """
        Remove the buffer size.
        """
        self._buffer_size = -1
        self.log(f"buffer_size.setter: Buffer_size has been removed (-1)")

    @property
    def main_buffer(self) -> list:
        """
        Get the main buffer.

        :return: The main buffer.
        :rtype: list
        """
        return self._main_buffer

    @main_buffer.setter
    def main_buffer(self, e: numpy) -> None:
        """
        Set the main buffer.

        :param e: The frame to add to the main buffer.
        :type e: numpy
        """
        if self.is_active():
            if self.is_main_buffer_full():
                if self.is_debugging():
                    self.dropped_frames += 1
            else:
                if self.is_debugging():
                    if self.dropped_frames > 0:
                        self.log(f"main_buffer.setter: {self.dropped_frames} frame(s) dropped")
                        self.dropped_frames = 0
                self.main_buffer.append(e)

    @main_buffer.deleter
    def main_buffer(self) -> None:
        """
        Clear the main buffer.
        """
        self._main_buffer.clear()
        self.log("main_buffer.deleter: main_buffer cleared")

    def is_active(self) -> bool:
        """
        Check if the buffer_size is set

        :return: True if active, False otherwise.
        :rtype: bool
        """
        return self.buffer_size != -1

    def is_main_buffer_full(self) -> bool:
        """
        Check if the main buffer is full.

        :return: True if the main buffer is full, False otherwise.
        :rtype: bool
        """
        return len(self.main_buffer) >= self.buffer_size

    def _mainloop(self) -> None:
        """
        The main loop for processing frames.
        """
        while self.is_running():
            if self.is_active():
                if self.target is True:
                    if len(self.main_buffer) > 0:
                        self.capture_frame = self.get_detection(self.main_buffer[len(self.main_buffer)-1]).draw_rectangle()
                else:
                    time.sleep(0.1)
                if self.is_main_buffer_full():
                    if self.get_detection(self.main_buffer[0]).is_card():
                        self._run()
                    del self.main_buffer
            else:
                time.sleep(0.1)

    def get_detection(self, frame) -> Detector:
        """
        Get the detector based on the detection option.

        :param frame: The frame to perform detection on.
        :return: The specific detector object
        :rtype: Detector
        """
        if self.detection_option == 1:
            return HMLDetector(frame)

    def _run(self) -> None:
        """
        Run the processing and detect student information from the best frame
        """
        detectors = [self.get_detection(self.main_buffer[i]) for i in range(10)]

        highest_quality = 0
        index = 0
        for i, v in enumerate(detectors):
            quality = v.quality
            if quality > highest_quality:
                highest_quality = quality
                index = i

        data = detectors[index].get_data()

        if data is None:
            self.mediator = "Student Card could not be read"
            self.log("run(): Data was None")
        else:
            try:
                self._students.students_list = data
                self.mediator = f"Student '{data['last_name']} {data['first_name']}' has been added"
            except AddingStudentError as error:
                self.log(f"run(): {error}")
            except MaxSeatError:
                self.mediator = f"Must set Max seat first"

    def start(self) -> None:
        """
        Start the processing thread.
        """
        self.log("start(): Thread started")
        super().start()

    def stop(self) -> None:
        """
        Stop the processing thread.
        """
        self.log("stop(): Thread stopped")
        super().stop()

    def __del__(self):
        """
        Destructor
        """
        self.log("-------------------")