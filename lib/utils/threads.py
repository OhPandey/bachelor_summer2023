import threading
from abc import ABC, abstractmethod

from lib.utils.exceptions import ThreadingError


class Threading(ABC):

    def __init__(self):
        self.thread = None
        self._running = False

    @abstractmethod
    def start(self) -> None:
        if self._running:
            raise ThreadingError("Attempted to start a thread while it was already running")

        self._change_running()
        self.thread = threading.Thread(target=self._mainloop)
        self.thread.start()

    @abstractmethod
    def stop(self) -> None:
        if not self._running:
            raise ThreadingError("Attempted to stop a thread while it was not running")

        self._change_running()
        self.thread.join()

    @abstractmethod
    def _mainloop(self) -> None:
        pass

    def _change_running(self) -> None:
        self._running = not self._running

    def is_running(self) -> bool:
        return self._running
