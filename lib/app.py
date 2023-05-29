from lib.data.students import Students
from lib.main_components.gui import GUI
from lib.main_components.processing import Processing
from lib.main_components.capturing import Capturing


class App:

    def __init__(self, channel=0):
        self.students = Students()
        self.processing = Processing(self.students)
        self.capturing = Capturing(channel)
        self.mainframe = GUI(self.students)
        self.start_session()

    def update(self):
        self.mainframe.stream(self.capturing.capture_frame)
        self.mainframe.students_list.update_students()
        self.mainframe.after(int(1000 / self.capturing.fps), self.update)

    def start_session(self) -> None:
        self.capturing.processing = self.processing
        self.processing.start()
        self.capturing.start()
        self.update()
        self.mainframe.mainloop()
        self.exit()

    def exit(self) -> None:
        if self.capturing is not None:
            self.capturing.stop()
        if self.processing is not None:
            self.processing.stop()
