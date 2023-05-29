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
        self.assign_mediators()
        self.start_session()

    def update(self, event: int, frame=None) -> None:
        if event == 1:
            self.mainframe.students_list.update()
        if event == 2:
            # NYI Update image
            return

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
