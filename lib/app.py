import tkinter as tk
import cv2
from PIL import Image, ImageTk

from lib.data.students import Students
from lib.threads.processing import Processing
from lib.threads.capturing import VideoCapture


class App:
    def __init__(self, video_source=0):
        self.analyzer = None
        self.videostream = None
        self.mainframe = None
        self.students = Students(10)
        self.video_source = video_source
        self.start_components()

    def update(self):
        videoframe = self.videostream.frame
        if videoframe is not None:
            videoframe = cv2.cvtColor(videoframe, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(videoframe)
            self.photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # print("List of running threads:", threading.enumerate())
        self.mainframe.after(self.videostream.delay, self.update)

    def is_videosource(self):
        return type(self.video_source) == int and self.video_source >= 0

    def start_components(self):
        if not self.is_videosource():
            raise ValueError(f"Videos_source {self.video_source} is not a valid stream")
        else:
            try:
                self.start_analyzer()
                self.start_videostream()
                self.start_frame()
            except:
                print('Something went wrong. Closing...')
                self.on_exit()

    def start_analyzer(self):
        self.analyzer = Processing(self.students)
        self.analyzer.start()

    def start_videostream(self):
        if self.analyzer is None:
            raise Exception
        self.videostream = VideoCapture(self.analyzer, self.video_source)
        self.videostream.start()

    def start_frame(self):
        if self.analyzer is None:
            raise Exception
        if self.videostream is None:
            raise Exception
        self.mainframe = tk.Tk()
        self.canvas = tk.Canvas(self.mainframe, width=self.videostream.width, height=self.videostream.height)
        self.canvas.pack()
        self.mainframe.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.update()
        self.mainframe.mainloop()

    def on_exit(self):
        if self.analyzer is not None:
            self.analyzer.stop()
        if self.videostream is not None:
            self.videostream.stop()
        if self.mainframe is not None:
            self.mainframe.destroy()
