import time
import cv2

from lib.debugging.subdirectory import Subdirectory
from lib.mediator.component import Component
from lib.threads.processing import Processing
from lib.debugging.debugging import Debugging
from lib.utils.exceptions import CameraNotAvailable, ProcessingNotAvailableError
from lib.utils.threads import Threading


class Capturing(Threading, Debugging, Component):
    _capture: "VideoCapture | None" = None
    _capture_frame: "numpy | None" = None
    _processing: "Processing | None" = None

    width: int = None
    height: int = None
    fps: int = None

    def __init__(self, channel: int):
        Threading.__init__(self)
        Debugging.__init__(self, Subdirectory.CAPTURING)
        self.capture = channel

    @property
    def capture(self):
        return self._capture

    @capture.setter
    def capture(self, channel: int) -> None:
        self._capture = cv2.VideoCapture(channel)
        if self._capture.isOpened():
            self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        else:
            del self.capture
            raise CameraNotAvailable

    @capture.deleter
    def capture(self) -> None:
        if self._capture:
            self._capture.release()
        self._capture = None
        self.width = -1
        self.height = -1
        self.fps = -1

    def is_active(self) -> bool:
        return self.capture is not None

    @property
    def processing(self) -> Processing | None:
        return self._processing

    @processing.setter
    def processing(self, processing: Processing) -> None:
        if self._processing is not None:
            self.log(f"add_processing(): Processing is already assigned")
            raise ProcessingNotAvailableError()

        self._processing = processing
        self._processing.buffer_size = self.fps

    @processing.deleter
    def processing(self) -> None:
        if self._processing is None:
            self.log(f"remove_processing(): Tried to remove an empty processing")
            raise ProcessingNotAvailableError()

        del self.processing.buffer_size
        self._processing = None

    def is_processing(self):
        return self.processing is not None

    def _mainloop(self) -> None:
        while self._running:
            if self.is_active():
                ret, frame = self.capture.read()
                if ret:
                    self.capture_frame = frame
                    if self.is_processing():
                        self.processing.add_queue(self.capture_frame)
                else:
                    del self.capture
                    self.log("Lost camera connection")
            else:
                time.sleep(0.1)

    def release(self) -> None:
        if self.is_processing():
            del self.processing
        if self.is_active():
            del self.capture

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()
        self.release()

    def __del__(self):
        self.release()
