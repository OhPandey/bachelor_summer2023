import tkinter
import tkinter.messagebox
import customtkinter


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Student Card Scanner.py")
        self.geometry(f"{1600}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

