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
        self.countFrame = 1
        self.normalAllowedFrame = 5
        self.bufferSize = 10
        self.mainBuffer = list()
        self.overflowBuffer = list()

    def start(self):
        super().start()

    def set_fps(self, value):
        self.fps = value

    def stop(self):
        super().stop()

    def isMainBufferFull(self):
        return len(self.mainBuffer) >= self.bufferSize

    def isOverflowBufferFull(self):
        return len(self.overflowBuffer) >= self.bufferSize

    def flush(self):
        self.mainBuffer.clear()
        self.mainBuffer = self.overflowBuffer[-10:]
        if len(self.overflowBuffer) >= 10:
            print(f"Frames removed:{len(self.overflowBuffer) - 10}")
        self.overflowBuffer.clear()

    def _mainloop(self):
        while self._running:
            if self.isMainBufferFull():
                if self.isFirstFrameStudentCard():
                    self.runProcesses()

                self.flush()
            else:
                time.sleep(0.1)

    def isFirstFrameStudentCard(self):
        return HMLDetector(0, self.mainBuffer[0], None).isAcceptableStudentCard()

    def runProcesses(self):
        queue = Queue()
        processes = list()
        for i in range(10):
            print(i)
            detector = HMLDetector(i, self.mainBuffer[i], queue)
            process = Process(target=detector.printFrameWithText)
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        results = [result for index, result in sorted([queue.get() for i in range(10)])]
        print(results)

    def addQueue(self, e):
        if not self.isMainBufferFull():
            self.mainBuffer.append(e)
        else:
            self.overflowBuffer.append(e)
