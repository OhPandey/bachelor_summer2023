import threading
from abc import ABC, abstractmethod


class Threading(ABC):

    def __init__(self):
        self.thread = None
        self._running = False

    @abstractmethod
    def start(self):
        if not self._running:
            self._running = True
            self.thread = threading.Thread(target=self._mainloop)
            self.thread.start()
        else:
            raise ValueError("Attempted to start a thread while it was already running")

    @abstractmethod
    def stop(self):
        if self._running:
            self._running = False
            self.thread.join()
        else:
            raise ValueError("Attempted to stop a thread while it was not running")

    @abstractmethod
    def _mainloop(self):
        pass
