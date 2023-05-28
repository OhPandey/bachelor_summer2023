import threading
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

from lib.data.students import Students
from lib.debugging.log import delete_log_all
from lib.threads.gui import GUI
from lib.threads.processing import Processing
from lib.threads.capturing import Capturing


class App:
    def __init__(self, video_source=0):
        self.processing = None
        self.capturing = None
        self.mainframe = None
        self.students = Students(10)
        self.video_source = video_source
        self.start_session()

    def start_session(self):
        self.processing = Processing(self.students)
        self.processing.set_debugging(True)
        self.processing.start()
        self.processing.stop()

