from lib.data.students import Students
from lib.debugging import config
from lib.interfaces.mediator.mediator import Mediator
from lib.main_components.gui import GUI
from lib.main_components.processing import Processing
from lib.main_components.capturing import Capturing


class App(Mediator):

    def __init__(self, channel=0):
        self.students = Students()
        self.processing = Processing(self.students)
        self.capturing = Capturing(channel)
        self.mainframe = GUI(self.students)
        self.response = ""
        self._target = config.get_config('project', 'show_target')
        self.start_session()

    @property
    def target(self) -> bool:
        if self._target == "True":
            return True
        return False

    def stream(self):
        if self.target:
            self.mainframe.stream(self.processing.capture_frame)
        else:
            self.mainframe.stream(self.capturing.capture_frame)
        self.mainframe.after(int(1000 / self.capturing.fps), self.stream)

    def update_gui(self):
        self.mainframe.students_list.update_students()
        self.mainframe.update()
        self.mainframe.set_seat_text(self.students.seat_list)
        if self.response != "":
            self.mainframe.info_label.configure(text=self.response)
            self.response = ""
        self.mainframe.after(500, self.update_gui)

    def set_response(self, text: str) -> None:
        self.response = text

    def assign(self):
        self.processing.mediator = self
        self.capturing.mediator = self

    def start_session(self) -> None:
        self.capturing.processing = self.processing
        self.processing.start()
        self.capturing.start()
        self.assign()
        self.stream()
        self.update_gui()
        self.mainframe.mainloop()
        self.exit()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
        if self.processing is not None:
            self.processing.stop()
