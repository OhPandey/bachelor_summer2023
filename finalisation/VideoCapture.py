import cv2

from finalisation.Interfaces.Threading import Threading


class VideoCapture(Threading):

    def __init__(self, process, video_source=0):
        super().__init__()

        self.video_source = video_source
        self.capture = cv2.VideoCapture(video_source)

        if not self.capture.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        self.delay = int(1000 / self.fps)

        self.frame = None
        self.process = process
        self.process.set_fps(self.fps)

    def start(self):
        super().start()

    def stop(self):
        super().stop()

    def _mainloop(self):
        while self._running:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
                self.process.addQueue(self.frame)
            else:
                self.stop()
                self.process.stop()
                break

    def get_frame(self):
        return self.frame

    def get_fps(self):
        return self.fps

    def get_delay(self):
        return self.delay

    def __del__(self):
        if self.capture:
            self.capture.release()
            self.capture = None
