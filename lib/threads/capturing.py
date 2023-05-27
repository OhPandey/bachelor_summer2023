import time

import cv2

from lib.threads.processing import Processing
from lib.utils.exceptions import CameraNotAvailable, ProcessingNotAvailableError, CapturingNotAvailableError
from lib.utils.threads import Threading


class Capturing(Threading):
    processing: "Processing | None" = None
    capture: "VideoCapture | None" = None
    capture_frame: "numpy | None" = None

    width: "int | None" = None
    height: "int | None" = None
    fps: "int | None" = None

    def __init__(self, channel: int):
        super().__init__()
        self.add_capture(channel)

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()
        self.release()

    def is_active(self) -> bool:
        return self.capture is not None

    def add_capture(self, channel) -> None:
        self.capture = cv2.VideoCapture(channel)
        if self.capture.isOpened():
            self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        else:
            self.capture = None
            self.width = None
            self.height = None
            self.fps = None
            raise CameraNotAvailable

    def remove_capture(self) -> None:
        if not self.capture:
            raise CameraNotAvailable

        self.capture.release()
        self.capture = None
        self.width = None
        self.height = None
        self.fps = None

    def add_processing(self, processing: Processing | None) -> None:
        if processing is None:
            raise ProcessingNotAvailableError("Adding an empty processing is not possible")

        if self.processing is not None:
            raise ProcessingNotAvailableError("Processing is already used")

        self.processing = processing
        self.processing.buffer_size = self.fps

    def remove_processing(self) -> None:
        if self.processing is None:
            raise ProcessingNotAvailableError("Removing an empty processing is not possible")

        self.processing.buffer_size = None
        self.processing = None

    def _mainloop(self) -> None:
        while self._running:
            if self.is_active():
                ret, frame = self.capture.read()
                if ret:
                    self.capture_frame = frame
                    if self.processing is not None:
                        self.processing.add_queue(self.capture_frame)
                else:
                    self.remove_capture()
            else:
                time.sleep(0.1)

    def release(self) -> None:
        if self.processing is not None:
            self.remove_processing()
        if self.capture is not None:
            self.remove_capture()

    def __del__(self):
        self.release()
