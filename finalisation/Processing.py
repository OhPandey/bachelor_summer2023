import os
import threading
import time
from multiprocessing import Process, Queue

from finalisation.Detectors.HMLDetector import HMLDetector
from finalisation.Interfaces.Threading import Threading


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
                firstframe = self.mainbuffer[0]
                detector = self.get_detection(firstframe)
                if detector.is_acceptable_student_card():
                    self._run()
                self.flush()
            else:
                time.sleep(0.1)

    def get_detection(self, frame, queue=None):
        if self.detectionoption == 1:
            return HMLDetector(frame, queue)

    def _run(self):
        queue = Queue()
        processes = list()
        for i in range(10):
            detector = self.get_detection(self.mainbuffer[i], queue)
            process = Process(target=detector.queue_quality(i))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        results = [queue.get() for i in range(10)]
        best = self._find_best_result(results)
        data = self.get_detection(self.mainbuffer[best]).retrieve_data()
        print(data)

    def _find_best_result(self, array):
        best = 0
        for i in array:
            id, value = i

            if value > array[best][1]:
                best = id
        return best

    def add_queue(self, e):
        if not self.is_mainbufferfull():
            self.mainbuffer.append(e)
        else:
            self.overflowbuffer.append(e)
