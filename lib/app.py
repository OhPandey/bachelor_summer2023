import time

from lib.data.students import Students
from lib.debugging import config
from lib.debugging.log import write_log
from lib.debugging.subdirectory import Subdirectory
from lib.interfaces.mediator.responsemediator import ResponseMediator
from lib.main_components.gui import GUI
from lib.main_components.processing import Processing
from lib.main_components.capturing import Capturing


class App(ResponseMediator):
    processing_time = None
    capturing_time = None

    def __init__(self, channel=0):
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
        if self.target:
            self.gui.stream(self.processing.capture_frame)
        else:
            self.gui.stream(self.capturing.capture_frame)
        self.gui.after(int(1000 / self.capturing.fps), self.stream)

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
            write_log(f"Processing Thread could not be started", Subdirectory.APPLICATION)

        if self.capturing is not None:
            self.capturing.processing = self.processing
            self.capturing.mediator = self
            self._start_capturing()
        else:
            write_log(f"Capturing Thread could not be started", Subdirectory.APPLICATION)

        if self.gui is not None:
            self._start_gui()
        else:
            write_log(f"GUI Thread could not be started", Subdirectory.APPLICATION)

        self.exit()

    def _start_processing(self) -> None:
        self.processing.start()
        self.processing_time = time.time()
        write_log(f"Processing Thread started", Subdirectory.APPLICATION)

    def _start_capturing(self) -> None:
        self.capturing.start()
        self.capturing_time = time.time()
        write_log(f"Capturing Thread started", Subdirectory.APPLICATION)

    def _start_gui(self) -> None:
        self.stream()
        self.update_gui()
        self.gui.mainloop()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
            if self.capturing_time is not None:
                write_log(f"Capturing Thread closed after {round(time.time()-self.capturing_time, 3)} seconds",
                          Subdirectory.APPLICATION)

        if self.processing is not None:
            self.processing.stop()
            if self.processing_time is not None:
                write_log(f"Processing Thread closed after {round(time.time()-self.processing_time, 3)} seconds",
                          Subdirectory.APPLICATION)

        write_log(f"-------------------", Subdirectory.APPLICATION)
