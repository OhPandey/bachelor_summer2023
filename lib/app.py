from lib.data.students import Students
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
        self.start_session()

    def update_gui(self):
        self.mainframe.stream(self.capturing.capture_frame)
        self.mainframe.students_list.update_students()
        if self.response != "":
            self.mainframe.info_label.configure(text=self.response)
            self.response = ""
        self.mainframe.after(int(1000 / self.capturing.fps), self.update_gui)

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
        self.update_gui()
        self.mainframe.mainloop()
        self.exit()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
        if self.processing is not None:
            self.processing.stop()
