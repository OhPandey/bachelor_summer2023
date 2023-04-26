import threading
import tkinter as tk
import cv2
from PIL import Image, ImageTk

from finalisation.Processing import Processing
from finalisation.VideoCapture import VideoCapture


# First iteration of the Application. It is using Multi-threading. GUI is not yet designed.
class App:
    def __init__(self, video_source=0):
        self.startComponents(video_source)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.videostream.width, height=self.videostream.height)
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.update()
        self.root.mainloop()

    def update(self):
        frame = self.videostream.get_frame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        #print("List of running threads:", threading.enumerate())
        self.root.after(self.videostream.get_delay(), self.update)

    def startComponents(self, video_source):
        self.process = Processing()
        self.videostream = VideoCapture(self.process, video_source)
        self.videostream.start()
        self.process.start()

    def on_exit(self):
        self.process.stop()
        self.videostream.stop()
        self.root.destroy()
