import tkinter
import tkinter.messagebox
import customtkinter


class GUI(customtkinter.CTk):
    def __init__(self, students):
        super().__init__()

        self.students = students
        # configure window
        self.title("Student Card Scanner.py")
        self.geometry(f"{1500}x{750}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="List of students",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=5, pady=(10, 10))
        self.students_list = ScrollableLabelButtonFrame(master=self.sidebar_frame,
                                                        students=self.students,
                                                        width=250, height=600,
                                                        corner_radius=0)
        self.students_list.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.max_seat_label = customtkinter.CTkLabel(self.sidebar_frame, text="Max seat:", justify="left",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.max_seat_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="CTkEntry", width=180)
        self.entry.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        self.main_button = customtkinter.CTkButton(self.sidebar_frame, text="Change", width=50, command=self.button_event)
        self.main_button.grid(row=3, column=0, padx=10, pady=20, sticky="e")

        self.capture_frame = customtkinter.CTkFrame(self)
        self.capture_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.test_label = customtkinter.CTkLabel(self.capture_frame,
                                                 text="Test",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
                                                 justify="center"
                                                 )
        self.test_label.grid(row=0, column=1, padx=10, pady=20)

    def button_event(self):
        # Logic missing here
        print(self.entry.get())


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, students, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.students = students
        self.command = command
        self.label_list = []
        self.button_list = []

    def update(self):
        diff = len(self.students.students) - len(self.label_list)
        if diff > 0:
            for i in range(-diff, 0):
                self.add_item(self.students.students[i])

    def add_item(self, e):
        # As Python is doing call by reference by default, i have to cast it to call by value here.
        text = f"Seat: {e.seat}\n{e.student_id}\n{e.last_name}"
        id = e.student_id
        label = customtkinter.CTkLabel(self, text=text,
                                       compound="left",
                                       padx=5, justify="left", anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button = customtkinter.CTkButton(self, text="Remove", width=50, height=50)
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        button.configure(
            command=lambda: self.remove_item(text, id))
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item, id):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                self.students.remove_student_by_id(id)
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
