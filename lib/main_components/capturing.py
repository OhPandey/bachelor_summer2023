import time
import cv2

from lib.debugging.subdirectory import Subdirectory
from lib.interfaces.mediator.component import Component
from lib.main_components.processing import Processing
from lib.debugging.debugging import Debugging
from lib.utils.exceptions import CameraNotAvailable, ProcessingNotAvailableError
from lib.interfaces.thread.thread import Thread


class Capturing(Thread, Debugging, Component):
    _capture: "VideoCapture | None" = None
    capture_frame: "numpy | None" = None
    _processing: "Processing | None" = None

    width: int = None
    height: int = None
    fps: int = None

    def __init__(self, channel: int):
        """
        Constructor

        :param channel: The channel number for the video capture.
        :type channel: int
        """
        Thread.__init__(self)
        Debugging.__init__(self, Subdirectory.CAPTURING)
        self.log("__init__(): Started")
        self.capture = channel

    @property
    def capture(self) -> cv2.VideoCapture | None:
        """
        Get the video capture instance.

        :return: The video capture instance.
        :rtype: VideoCapture | None
        """
        return self._capture

    @capture.setter
    def capture(self, channel: int) -> None:
        """
        Set the video capture instance.

        :param channel: The channel number for the video capture.
        :type channel: int
         """
        self._capture = cv2.VideoCapture(channel)
        if self._capture.isOpened():
            self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
            self.log(f"capture.setter: Capture with channel {channel} initialized. "
                     f"Width: {self.width}, Height: {self.height}, FPS: {self.fps}")
        else:
            del self.capture
            self.log(f"Capture with channel {channel} not available.")
            raise CameraNotAvailable

    @capture.deleter
    def capture(self) -> None:
        """
        Release the video capture instance.
        """
        if self._capture:
            self.log(f"capture.deleter: Capture released.")
            self._capture.release()
        self._capture = None
        self.width = -1
        self.height = -1
        self.fps = -1

    def is_active(self) -> bool:
        """
        Check if the video capture instance is active.

        :return: True if video capture instance is active, False otherwise.
        :rtype: bool
        """
        return self.capture is not None

    @property
    def processing(self) -> Processing | None:
        """
        Get the processing instance.

        :return: The processing instance.
        :rtype: Processing | None
        """
        return self._processing

    @processing.setter
    def processing(self, processing: Processing) -> None:
        """
        Set the processing instance.

        :param processing: The processing instance.
        :type processing: Processing
        """
        if self._processing is not None:
            self.log(f"processing.setter: Tried to add a processing that was already active")
            raise ProcessingNotAvailableError()

        self._processing = processing
        self._processing.buffer_size = self.fps
        self.log(f"processing.setter: Processing added. Set Buffer_size to {self.fps}")

    @processing.deleter
    def processing(self) -> None:
        """
        Delete the processing instance.
        """
        if not self.is_processing():
            self.log(f"remove_processing(): Tried to remove an processing that is None")
            raise ProcessingNotAvailableError()

        del self.processing.buffer_size
        self._processing = None
        self.log(f"processing.deleter: Processing removed")

    def is_processing(self):
        """
        Check if the processing instance is active

        :return: True if the processing instance is active, False otherwise.
        :rtype: bool
        """
        return self.processing is not None

    def _mainloop(self) -> None:
        """
        Main loop for capturing frames (and sending them to processing).
        """
        while self._running:
            if self.is_active():
                ret, frame = self.capture.read()
                if ret:
                    self.capture_frame = frame
                    if self.is_processing():
                        self.processing.main_buffer = self.capture_frame
                else:
                    del self.capture
                    self.log("mainloop(): Lost camera connection")
            else:
                time.sleep(0.1)

    def release(self) -> None:
        """
        Release resources.
        """
        if self.is_processing() or self.is_active():
            self.log("release(): Releasing resources")
        if self.is_processing():
            del self.processing
        if self.is_active():
            del self.capture

    def start(self) -> None:
        """
        Start the capturing thread
        """
        self.log("start(): Thread started")
        super().start()

    def stop(self) -> None:
        """
        Stop the capturing thread.
        """
        self.log("stop(): Thread stopped")
        super().stop()
        self.release()

    def __del__(self):
        """
        Destructor
        """
        self.release()
        self.log("-------------------")
