import os
import tkinter
import tkinter.messagebox
import customtkinter
import cv2
from PIL import Image, ImageTk


class GUI(customtkinter.CTk):
    def __init__(self, students):
        super().__init__()
        self.camera_found = False
        self.students = students
        # configure window
        self.title("Student Card Scanner.py")
        self.geometry(f"{1400}x{650}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Side frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=120, corner_radius=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        # Student List Title Widget
        self.list_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="List of students",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.list_label.grid(row=0, column=0, padx=5, pady=(10, 10))
        # Student List Widget
        self.students_list = ScrollableLabelButtonFrame(master=self.sidebar_frame,
                                                        students=self.students,
                                                        width=200, height=400,
                                                        corner_radius=0)
        self.students_list.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        # Maximum Seat Title Widget
        self.max_seat_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                     text="",
                                                     justify="left",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.max_seat_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        # Maximum Seat Input Widget
        self.max_seat_input = customtkinter.CTkEntry(self.sidebar_frame,
                                                     placeholder_text="Type available seats",
                                                     width=130)
        self.max_seat_input.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        # Maximum Seat Button Widget
        self.max_seat_button = customtkinter.CTkButton(self.sidebar_frame,
                                                       text="Set",
                                                       width=60,
                                                       command=self.max_set_button_event)
        self.max_seat_button.grid(row=3, column=0, padx=10, pady=20, sticky="e")

        # Saving

        self.save_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Save as",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.save_label.grid(row=4, column=0, padx=10, sticky="n")

        self.pdf_button = customtkinter.CTkButton(self.sidebar_frame,
                                                  text="PDF",
                                                  width=60,
                                                  command=self.save_as_pdf)
        self.pdf_button.grid(row=4, column=0, padx=10, pady=20, sticky="sw")
        self.csv_button = customtkinter.CTkButton(self.sidebar_frame,
                                                  text="CSV",
                                                  width=60,
                                                  command=self.save_as_csv)
        self.csv_button.grid(row=4, column=0, padx=(78, 0), pady=20, sticky="sw")

        self.json_button = customtkinter.CTkButton(self.sidebar_frame,
                                                   text="Json",
                                                   width=60,
                                                   command=self.save_as_json)
        self.json_button.grid(row=4, column=0, padx=(10, 10), pady=20, sticky="se")

        # Main frame
        self.capture_frame = customtkinter.CTkFrame(self)
        self.capture_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # Interactive Response Label Widget
        self.info_label = customtkinter.CTkLabel(self.capture_frame,
                                                 text="Camera not found",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"),
                                                 width=1200)
        self.info_label.grid(row=0, column=0, padx=5, pady=(10, 10))
        # Camera Widget
        default_image = customtkinter.CTkImage(Image.open('video-not-working.png'), size=(635, 328))
        self.stream_label = customtkinter.CTkLabel(self.capture_frame,
                                                   text="",
                                                   image=default_image)
        self.stream_label.grid(row=1, column=0, padx=20, pady=10)

    def save_as_pdf(self):
        if len(self.students.students_list) > 0:
            self.students.save_as_pdf()
            del self.students.students_list
            del self.students.seat_list
            self.students_list.remove_all()

    def save_as_csv(self):
        if len(self.students.students_list) > 0:
            self.students.save_as_csv()
            del self.students.students_list
            del self.students.seat_list
            self.students_list.remove_all()

    def save_as_json(self):
        if len(self.students.students_list) > 0:
            self.students.save_as_json()
            del self.students.students_list
            del self.students.seat_list
            self.students_list.remove_all()

    def stream(self, capture):
        if capture is not None:
            h, w, z = capture.shape
            if self.camera_found is False:
                self.set_info_text("Students Card Detector")
                self.camera_found = True
                self.geometry(f"{w + 950}x{self.winfo_height()}")

            if self.winfo_height() < 650:
                self.geometry(f"{self.winfo_width()}x{650}")

            if self.winfo_width() < (w + 950):
                self.geometry(f"{w + 950}x{self.winfo_height()}")
            img = Image.fromarray(cv2.cvtColor(capture, cv2.COLOR_BGR2RGB))
            de = customtkinter.CTkImage(img, size=(
                self.capture_frame.winfo_width() - 40, self.capture_frame.winfo_height() - 100))

            self.stream_label.configure(image=de)

    def set_info_text(self, text: str):
        self.info_label.configure(text=text)

    def set_seat_text(self, number: int):
        if number == -1:
            self.max_seat_label.configure(text="How many seats?")
        else:
            self.max_seat_label.configure(text=f"{str(number)}/{str(self.students.max_seat)} seats available")

    def update(self):
        if self.students.is_seat_list():
            self.pdf_button.configure(state="normal")
            self.csv_button.configure(state="normal")
            self.json_button.configure(state="normal")
            self.max_seat_button.configure(state="disabled")
            self.max_seat_input.configure(state="disabled")
        else:
            self.pdf_button.configure(state="disabled")
            self.csv_button.configure(state="disabled")
            self.json_button.configure(state="disabled")
            self.max_seat_button.configure(state="normal")
            self.max_seat_input.configure(state="normal")

    def max_set_button_event(self):
        if self.max_seat_input.get() == "":
            return
        if not self.max_seat_input.get().isnumeric():
            self.set_info_text("Max seat has to be a number")
            return

        seat_number = int(self.max_seat_input.get())
        self.max_seat = seat_number
        self.students.seat_list = seat_number


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
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

    def remove_all(self):
        for label in self.label_list:
            label.destroy()
        self.label_list.clear()

        for button in self.button_list:
            button.destroy()
        self.button_list.clear()
