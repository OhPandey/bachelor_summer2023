import random
import json
import csv

from datetime import datetime
from lib.data.student import Student
from lib.utils.exceptions import AddingStudentError, MaxSeatError
from fpdf import FPDF
from lib.data.dataset import STUDENT_REQUIRED_KEYS


class Students:
    filename = "default-" + str(datetime.now().strftime("%y%m%d%H%M"))

    def __init__(self):
        self._students_list = list()
        self._seat_list = None

    # student_list functions
    @property
    def students_list(self) -> list:
        return self._students_list

    @students_list.setter
    def students_list(self, data: dict) -> None:
        if not all(key in data for key in STUDENT_REQUIRED_KEYS):
            array = []

            for key in STUDENT_REQUIRED_KEYS:
                if key not in data:
                    array.append(key)

            raise AddingStudentError("The dictionary given does not meet the required keys: " + str(array))

        if self.is_duplicate(data["student_id"]):
            raise AddingStudentError("The data given is a duplicate")

        if self.seat_list <= 0:
            raise MaxSeatError

        val = self._seat_list[random.randint(0, self.seat_list - 1)]
        self._seat_list.remove(val)
        data.update({"seat": val})

        self.students_list.append(Student(**data))

    @students_list.deleter
    def students_list(self):
        self._students_list.clear()

    def remove_student_by_element(self, e: Student) -> bool:
        try:
            self._seat_list.append(e.seat)
            self._students_list.remove(e)
            return True
        except ValueError:
            return False

    def remove_student_by_index(self, i: int) -> bool:
        try:
            self._seat_list.append(self._students_list[i])
            self._students_list.pop(i)
            return True
        except IndexError:
            return False

    def remove_student_by_student_id(self, student_id) -> bool:
        for i, x in enumerate(self._students_list):
            if x.student_id == student_id:
                self.remove_student_by_index(i)
                return True
        return False

    def is_duplicate(self, student_id) -> bool:
        for k in self.students_list:
            if k.student_id == student_id:
                return True

        return False

    # seat_list functions
    @property
    def seat_list(self) -> int | None:
        if self._seat_list is None:
            return -1
        return len(self._seat_list)

    @seat_list.setter
    def seat_list(self, size: int) -> None:
        self._seat_list = list(range(1, size+1))

    @seat_list.deleter
    def seat_list(self) -> None:
        self._seat_list = None

    def is_seat_list(self) -> bool:
        return self.seat_list >= 0

    # Saving file functions
    def set_filename(self, filename):
        self.filename = filename

    def save_as_pdf(self) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        for i, x in enumerate(self._students_list):
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
        for student in self._students_list:
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

        for student in self._students_list:
            data.append({
                "Name": f"{student.last_name} {student.first_name}",
                "Birthday": f"{student.birth_year}-{student.get_month_number()}-{student.birth_day}",
                "StudentID": student.student_id,
                "Seat": student.seat
            })

        with open(f"{self.filename}.json", "w") as file:
            json.dump(data, file)
