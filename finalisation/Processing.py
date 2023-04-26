import threading
import time
from multiprocessing import Process

from finalisation.Detectors.HMLDetector import HMLDetector
from finalisation.Interfaces.Threading import Threading


class Processing(Threading):
    def __init__(self):
        super().__init__()
        self.semaphore = threading.Semaphore(1)
        self.countFrame = 1
        self.normalAllowedFrame = 5
        self.maxbuffersize = 10
        self.buffer = list()

    def start(self):
        super().start()

    def stop(self):
        super().stop()

    def _mainloop(self):
        while self._running:
            if len(self.buffer) >= self.maxbuffersize:
                frame = self.buffer[0]
                if HMLDetector(frame).isStudentCard():
                    self.semaphore.acquire()
                    count = 0

                    for frame in self.buffer:
                        Process(target=HMLDetector(frame).print('debugging/image'+str(count)+'.jpg'))
                        count += 1

                    self.semaphore.release()
                    self.buffer.clear()
                else:
                    self.buffer.clear()
            else:
                time.sleep(0.1)


    def addQueue(self, e):
        self.buffer.append(e)
