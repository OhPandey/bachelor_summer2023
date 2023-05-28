import threading
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

from lib.data.students import Students
from lib.debugging.log import delete_log_all
from lib.mediator.mediator import Mediator
from lib.threads.gui import GUI
from lib.threads.processing import Processing
from lib.threads.capturing import Capturing


class App(Mediator):

    def __init__(self, channel=0):
        self.students = Students()
        self.processing = Processing(self.students)
        self.capturing = Capturing(channel)
        self.mainframe = GUI(self.students)
        self.assign_mediators()
        self.start_session()

    def update(self, event: str) -> None:
        self.mainframe.students_list.update()

    def assign_mediators(self):
        self.processing.mediator = self
        self.capturing.mediator = self

    def start_session(self) -> None:
        self.capturing.processing = self.processing
        self.processing.start()
        self.capturing.start()
        self.mainframe.mainloop()
        self.exit()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
        if self.processing is not None:
            self.processing.stop()
