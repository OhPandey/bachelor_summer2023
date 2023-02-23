from tkinter import *


class Window:

    def __init__(self, title: str = "Placeholder"):
        self.window = Tk()
        self.window.title(title)

    def show(self):
        self.window.mainloop()

    def end(self):
        self.window.destroy()
