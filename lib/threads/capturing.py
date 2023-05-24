import cv2

from lib.utils.threading import Threading


class VideoCapture(Threading):

    def __init__(self, process, video_source):
        super().__init__()

        self.video_source = video_source
        self.capture = cv2.VideoCapture(video_source)

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
        self.release()

    def release(self):
        if self.capture:
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
                break

    def __del__(self):
        self.release()
