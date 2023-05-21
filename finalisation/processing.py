import os
import threading
import time
from multiprocessing import Process, Queue

from finalisation.Detectors.hmldetector import HMLDetector
from finalisation.Interfaces.threading import Threading


class Processing(Threading):
    def __init__(self):
        super().__init__()
        self.fps = None
        self.countframes = 1
        self.buffersize = 10
        self.mainbuffer = list()
        self.overflowbuffer = list()
        self.detectionoption = 1

    def start(self):
        super().start()

    def set_fps(self, value):
        self.fps = value

    def stop(self):
        super().stop()

    def is_mainbufferfull(self):
        return len(self.mainbuffer) >= self.buffersize

    def is_overflowbufferfull(self):
        return len(self.overflowbuffer) >= self.buffersize

    def flush(self):
        self.mainbuffer.clear()
        self.mainbuffer = self.overflowbuffer[-10:]
        # if len(self.overflowbuffer) >= 10:
        #    print(f"Frames dropped:{len(self.overflowbuffer) - 10}")
        self.overflowbuffer.clear()

    def _mainloop(self):
        while self._running:
            if self.is_mainbufferfull():
                detector = self.get_detection(self.mainbuffer[0])
                print(detector.check())
                self.flush()
            else:
                time.sleep(0.1)

    def get_detection(self, frame):
        if self.detectionoption == 1:
            return HMLDetector(frame)

    # def _run(self):
    #     detectors = list()
    #     for i in range(10):
    #         detectors.append(self.get_detection(self.mainbuffer[i]))

    def add_queue(self, e):
        if not self.is_mainbufferfull():
            self.mainbuffer.append(e)
        else:
            self.overflowbuffer.append(e)
