import threading
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

from lib.data.students import Students
from lib.threads.gui import GUI
from lib.threads.processing import Processing
from lib.threads.capturing import Capturing



class App:
    def __init__(self, video_source=0):
        self.analyzer = None
        self.video_stream = None
        self.mainframe = None
        self.students = Students(10)
        self.video_source = video_source
        self.start_session()

    def start_session(self):
        self.mainframe = GUI(self.students)
        self.students.add_student({
            "last_name": "DA SILVA GONCALVES VERRY LONG NAME HAHSA",
            "first_name": "Joey",
            "birth_day": "03",
            "birth_month": "May",
            "birth_year": "1997",
            "student_id": "0181039342"
        })
        self.students.add_student({
            "last_name": "ANOTHER LONG LANGE",
            "first_name": "Joey",
            "birth_day": "03",
            "birth_month": "May",
            "birth_year": "1997",
            "student_id": "0181049342"
        })
        self.students.add_student({
            "last_name": "WHATEVER",
            "first_name": "Joey",
            "birth_day": "03",
            "birth_month": "May",
            "birth_year": "1997",
            "student_id": "0181049352"
        })
        self.lol = threading.Thread(target=self.meme_loop)
        self.lol.start()
        self.mainframe.mainloop()

    def meme_loop(self):
        while True:
            self.mainframe.students_list.update()
            time.sleep(0.1)

    # def update(self):
    #     videoframe = self.video_stream.frame
    #     if videoframe is not None:
    #         videoframe = cv2.cvtColor(videoframe, cv2.COLOR_BGR2RGB)
    #         image = Image.fromarray(videoframe)
    #         self.photo = ImageTk.PhotoImage(image=image)
    #         self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
    #
    #         # print("List of running threads:", threading.enumerate())
    #     self.mainframe.after(self.video_stream.delay, self.update)
    #
    # def is_videosource(self):
    #     return type(self.video_source) == int and self.video_source >= 0
    #
    # def start_components(self):
    #     if not self.is_videosource():
    #         raise ValueError(f"Videos_source {self.video_source} is not a valid stream")
    #     else:
    #         try:
    #             self.start_analyzer()
    #             self.start_videostream()
    #             self.start_frame()
    #         except:
    #             print('Something went wrong. Closing...')
    #             self.on_exit()
    #
    # def start_analyzer(self):
    #     self.analyzer = Processing(self.students)
    #     self.analyzer.start()
    #
    # def start_videostream(self):
    #     if self.analyzer is None:
    #         raise Exception
    #     self.video_stream = VideoCapture(self.analyzer, self.video_source)
    #     self.video_stream.start()
    #
    # def start_frame(self):
    #     if self.analyzer is None:
    #         raise Exception
    #     if self.video_stream is None:
    #         raise Exception
    #     self.mainframe = tk.Tk()
    #     self.canvas = tk.Canvas(self.mainframe, width=self.video_stream.width, height=self.video_stream.height)
    #     self.canvas.pack()
    #     self.mainframe.protocol("WM_DELETE_WINDOW", self.on_exit)
    #     self.update()
    #     self.mainframe.mainloop()
    #
    # def on_exit(self):
    #     if self.analyzer is not None:
    #         self.analyzer.stop()
    #     if self.video_stream is not None:
    #         self.video_stream.stop()
    #     if self.mainframe is not None:
    #         self.mainframe.destroy()
