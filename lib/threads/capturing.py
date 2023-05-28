import time
import cv2

from lib.debugging.subdirectory import Subdirectory
from lib.threads.processing import Processing
from lib.debugging.debugging import Debugging
from lib.utils.exceptions import CameraNotAvailable, ProcessingNotAvailableError
from lib.utils.threads import Threading


class Capturing(Threading, Debugging):
    processing: "Processing | None" = None
    capture: "VideoCapture | None" = None
    capture_frame: "numpy | None" = None

    width: "int | None" = None
    height: "int | None" = None
    fps: "int | None" = None

    def __init__(self, channel: int):
        Threading.__init__(self)
        Debugging.__init__(self, Subdirectory.CAPTURING)
        self.add_capture(channel)

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()
        self.release()

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
            self.log(f"add_capture(): Camera on channel {channel} not found")
            raise CameraNotAvailable

    def remove_capture(self) -> None:
        if self.capture:
            self.capture.release()
        else:
            self.log("remove_capture(): There was no capture running")
        self.capture = None
        self.width = None
        self.height = None
        self.fps = None

    def is_active(self) -> bool:
        return self.capture is not None

    def add_processing(self, processing: Processing) -> None:
        if self.processing is not None:
            self.log(f"add_processing(): Processing is already assigned")
            raise ProcessingNotAvailableError()

        self.processing = processing
        self.processing.buffer_size = self.fps

    def remove_processing(self) -> None:
        if self.processing is None:
            self.log(f"remove_processing(): Tried to remove an empty processing")
            raise ProcessingNotAvailableError()

        self.processing.buffer_size = None
        self.processing = None

    def has_processing(self):
        return self.processing is not None

    def _mainloop(self) -> None:
        while self._running:
            self.log("Test.")
            if self.is_active():
                ret, frame = self.capture.read()
                if ret:
                    self.capture_frame = frame
                    if self.has_processing():
                        self.processing.add_queue(self.capture_frame)
                else:
                    self.remove_capture()
                    self.log("Lost camera connection")
            else:
                time.sleep(0.1)

    def release(self) -> None:
        if self.processing is not None:
            self.remove_processing()
        if self.capture is not None:
            self.remove_capture()

    def __del__(self):
        self.release()
