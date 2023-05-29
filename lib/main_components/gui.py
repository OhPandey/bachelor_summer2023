import os
import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk


class GUI(customtkinter.CTk):
    def __init__(self, students):
        super().__init__()
        self.students = students
        # configure window
        self.title("Student Card Scanner.py")
        self.geometry(f"{1500}x{750}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Side frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.list_label = customtkinter.CTkLabel(self.sidebar_frame, text="List of students",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.list_label.grid(row=0, column=0, padx=5, pady=(10, 10))
        self.students_list = ScrollableLabelButtonFrame(master=self.sidebar_frame,
                                                        students=self.students,
                                                        width=250, height=600,
                                                        corner_radius=0)
        self.students_list.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.max_seat_label = customtkinter.CTkLabel(self.sidebar_frame, text="How many seats?", justify="left",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.max_seat_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.max_seat_button = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Number", width=180)
        self.max_seat_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        self.main_button = customtkinter.CTkButton(self.sidebar_frame, text="Set", width=50,
                                                   command=self.max_set_button_event)
        self.main_button.grid(row=3, column=0, padx=10, pady=20, sticky="e")

        # Main frame
        self.capture_frame = customtkinter.CTkFrame(self)
        self.capture_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.info_label = customtkinter.CTkLabel(self.capture_frame, text="Test",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"),
                                                 width=1200)
        self.info_label.grid(row=0, column=0, padx=5, pady=(10, 10), sticky="")
        # image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.large_test_image = customtkinter.CTkImage(Image.open('video-not-working.png'), size=(1000, 500))
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.capture_frame, text="",
                                                                   image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=1, column=0, padx=20, pady=10)

    def stream(self, capture):
        if capture is not None:
            img = Image.fromarray(cv2.cvtColor(capture, cv2.COLOR_BGR2RGB))

            de = customtkinter.CTkImage(img, size=(self.capture_frame.winfo_width()-100, self.capture_frame.winfo_height()-100))

            self.home_frame_large_image_label.configure(image=de)

    def max_set_button_event(self):
        if self.max_seat_button.get() == "":
            return
        if not self.max_seat_button.get().isnumeric():
            self.info_label.configure(text="Max seat has to be a number")
            return
        self.info_label.configure(text=f"Max seat set to {self.max_seat_button.get()}")
        self.students.seat_list = int(self.max_seat_button.get())


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    # Doing this frame with customtkinter wasn't easy. Had to find a lot of workarounds
    def __init__(self, master, students, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.students = students
        self.command = command
        self.label_list = []
        self.button_list = []

    def update_students(self):
        if self.students.is_seat_list():
            diff = len(self.students.students_list) - len(self.label_list)
            if diff > 0:
                for i in range(-diff, 0):
                    self.add_item(self.students.students_list[i])

    def add_item(self, e):
        text = f"Seat: {e.seat}\n{e.student_id}\n{e.last_name}"
        student_id = e.student_id
        label = customtkinter.CTkLabel(self, text=text,
                                       compound="left",
                                       padx=5, justify="left", anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button = customtkinter.CTkButton(self, text="Remove", width=50, height=50)
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        button.configure(
            command=lambda: self.remove_item(text, student_id))
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item, student_id):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                self.students.remove_student_by_student_id(student_id)
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
