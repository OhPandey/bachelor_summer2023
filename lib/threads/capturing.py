import cv2

from lib.threads.processing import Processing
from lib.utils.exceptions import CameraNotAvailable
from lib.utils.threading import Threading


class Capturing(Threading):

    def __init__(self, process: Processing, video_source: int):
        super().__init__()
        self.capture = cv2.VideoCapture(video_source)

        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))

        self.frame = None
        self.process = process
        self.process.buffer_size = self.fps

    def start(self) -> None:
        super().start()

    def stop(self) -> None:
        super().stop()
        self.release()

    def release(self) -> None:
        if self.capture:
            self.process.buffer_size = None
            self.capture.release()
            self.capture = None

    def _mainloop(self):
        while self._running:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
                self.process.add_queue(self.frame)
            else:
                self.stop()
                self.process.stop()
                raise CameraNotAvailable

    def __del__(self):
        self.release()
