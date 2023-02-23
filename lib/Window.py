from tkinter import *


class Window:

    def __init__(self, title: str = "Placeholder"):
        self.window = Tk()
        self.window.title(title)
        self.window.geometry('400x300')

    def loop(self):
        self.window.mainloop()

    def show(self):
        def change():
            lbl.config(text="You did it!")
            message()

        lbl = Label(
            self.window,
            bg='#5f734c',
            font=18,
            text="Click the button the start!"
        )
        lbl.pack(expand=True)

        btn = Button(
            self.window,
            text='The button',
            padx=10,
            pady=5,
            command=change
        )
        btn.pack(expand=True)

        def message():
            print('Amazing!')

        self.loop()

    def end(self):
        self.window.destroy()
