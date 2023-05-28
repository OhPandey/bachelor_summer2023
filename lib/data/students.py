import random
import json
import csv

from datetime import datetime
from lib.data.student import Student
from lib.utils.exceptions import AddingStudentError, MaxSeatError
from fpdf import FPDF
from lib.data.datasets import check_student_directory


class Students:
    filename = "default-"+str(datetime.now().strftime("%y%m%d%H%M"))

    def __init__(self, max_seat: int):
        self.students_list = list()
        self.seat_list = list(range(max_seat))

    def add_student(self, data: dict):

        check = check_student_directory(data)
        if check is not None:
            raise AddingStudentError("The dictionary given does not meet the required keys: "+str(check))

        if self.is_duplicate(data["student_id"]):
            raise AddingStudentError("The data given is a duplicate")

        if self.get_max_seat() <= 0:
            raise MaxSeatError

        val = self.seat_list[random.randint(0, len(self.seat_list) - 1)]
        self.seat_list.remove(val)
        data.update({"seat": val})

        self.students_list.append(Student(**data))

        return True

    def get_max_seat(self) -> int:
        return len(self.seat_list)

    def is_duplicate(self, student_id) -> bool:
        for k in self.students_list:
            if k.student_id == student_id:
                return True

        return False

    def remove_student_by_element(self, e: Student) -> bool:
        try:
            self.seat_list.append(e.seat)
            self.students_list.remove(e)
            return True
        except ValueError:
            return False

    def remove_student_by_index(self, i: int) -> bool:
        try:
            self.seat_list.append(self.students_list[i])
            self.students_list.pop(i)
            return True
        except IndexError:
            return False

    def remove_student_by_student_id(self, student_id) -> bool:
        for i, x in enumerate(self.students_list):
            if x.student_id == student_id:
                self.remove_student_by_index(i)
                return True

        return False

    def set_filename(self, filename):
        self.filename = filename

    def save_as_pdf(self) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        for i, x in enumerate(self.students_list):
            if not isinstance(x, Student):
                text = f"<Error retrieving student#{i}>"
            else:
                text = f"{x.last_name} {x.first_name}, {x.birth_day}. {x.birth_month} {x.birth_year}, {x.student_id}, SEAT: {x.seat}"
            pdf.cell(200, 5, txt=text, ln=1)

        # Placeholder. User should be able to decide the directory
        pdf.output(f"{self.filename}.pdf")

    def save_as_csv(self) -> None:
        data = [
            [
                "Name",
                "Birthday",
                "Student ID",
                "Seat Number"
            ]
        ]
        for student in self.students_list:
            data.append([
                f"{student.last_name} {student.first_name}",
                f"{student.birth_year}-{student.get_month_number()}-{student.birth_day}",
                f"{student.student_id}",
                f"{student.seat}"
            ])

        with open(f"{self.filename}.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def save_as_json(self) -> None:

        data = []

        for student in self.students_list:
            data.append({
                "Name": f"{student.last_name} {student.first_name}",
                "Birthday": f"{student.birth_year}-{student.get_month_number()}-{student.birth_day}",
                "StudentID": student.student_id,
                "Seat": student.seat
            })

        with open(f"{self.filename}.json", "w") as file:
            json.dump(data, file)
