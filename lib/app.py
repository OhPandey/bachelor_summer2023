import time

import cv2

from lib.data.students import Students
from lib.debugging import config
from lib.debugging.debugging import Debugging
from lib.debugging.subdirectory import Subdirectory
from lib.interfaces.mediator.responsemediator import ResponseMediator
from lib.main_components.gui import GUI
from lib.main_components.processing import Processing
from lib.main_components.capturing import Capturing


class App(ResponseMediator, Debugging):
    processing_time = None
    capturing_time = None

    def __init__(self, channel=0):
        Debugging.__init__(self, Subdirectory.APPLICATION)
        self.log("__init__(): Started")

        self.students = Students()
        self.processing = Processing(self.students)
        self.capturing = Capturing(channel)
        self.gui = GUI(self.students)

        self.start_application()

    @property
    def target(self) -> bool:
        if config.get_config('project', 'show_target') == "True":
            return True
        return False

    def stream(self) -> None:
        if self.capturing.is_active():
            fps = self.capturing.fps
            if self.target:
                capture = self.processing.capture_frame
            else:
                capture = self.capturing.capture_frame
        else:
            print('Test?')
            capture = None
            fps = 30

        self.gui.stream(capture)
        self.gui.after(int(1000 / fps), self.stream)

    def update_gui(self) -> None:
        self.gui.students_list.update_students()
        self.gui.update()
        self.gui.set_seat_text(self.students.seat_list)
        if self.response is not None:
            self.gui.info_label.configure(text=self.response)
            self.response = None
        self.gui.after(500, self.update_gui)

    def start_application(self) -> None:
        if self.processing is not None:
            self.processing.mediator = self
            self._start_processing()
        else:
            self.log(f"Processing Thread could not be started")

        if self.capturing is not None:
            self.capturing.processing = self.processing
            self.capturing.mediator = self
            self._start_capturing()
        else:
            self.log(f"Capturing Thread could not be started")

        if self.gui is not None:
            self._start_gui()
        else:
            self.log(f"GUI Thread could not be started")

        self.exit()

    def _start_processing(self) -> None:
        self.processing.start()
        self.processing_time = time.time()
        self.log(f"Processing Thread started")

    def _start_capturing(self) -> None:
        self.capturing.start()
        self.capturing_time = time.time()
        self.log(f"Capturing Thread started")

    def _start_gui(self) -> None:
        self.stream()
        self.update_gui()
        self.gui.mainloop()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
            if self.capturing_time is not None:
                self.log(f"Capturing Thread closed after {round(time.time()-self.capturing_time, 3)} seconds")

        if self.processing is not None:
            self.processing.stop()
            if self.processing_time is not None:
                self.log(f"Processing Thread closed after {round(time.time()-self.processing_time, 3)} seconds")

        self.log(f"-------------------")
