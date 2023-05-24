import random
from fpdf import FPDF
import json
import csv
from finalisation.data.student import Student
from finalisation.lib.exceptions import AddingStudentError, MaxSeatError


class Students:
    filename = "default"

    def __init__(self, max_seat):
        self.students = list()
        self.seat_list = list(range(max_seat))

    def add_student(self, data):
        if not isinstance(data, dict):
            raise AddingStudentError("The data given is not an dictionary")

        if "last_name" not in data or "first_name" not in data or "birth_day" not in data or "birth_month" not in data or "birth_year" not in data or "student_id" not in data:
            raise AddingStudentError("The dictionary given is does not met the required keys: "
                                     "last_name, first_name, birth_day, birth_month, birth_year, student_id")

        if self.is_duplicate(data["student_id"]):
            raise AddingStudentError("The data given is a duplicate")

        if len(self.seat_list) <= 0:
            raise MaxSeatError

        val = self.seat_list[random.randint(0, len(self.seat_list) - 1)]
        self.seat_list.remove(val)

        self.students.append(
            Student(
                last_name=data["last_name"],
                first_name=data["first_name"],
                birth_day=data["birth_day"],
                birth_month=data["birth_month"],
                birth_year=data["birth_year"],
                student_id=data["student_id"],
                seat=val
            )
        )

    def is_duplicate(self, student_id) -> bool:
        for k in self.students:
            if k.student_id == student_id:
                return True

        return False

    def remove_student_by_element(self, e) -> bool:
        try:
            self.students.pop(e)
            return True
        except IndexError:
            return False

    def remove_student_by_id(self, student_by) -> bool:
        for i, x in enumerate(self.students):
            if x.getId() == student_by:
                self.remove_student_by_element(i)
                return True

        return False

    def set_filename(self, filename):
        self.filename = filename

    def save_as_pdf(self) -> None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        for i, x in enumerate(self.students):
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
        for student in self.students:
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

        for student in self.students:
            data.append({
                "Name": f"{student.last_name} {student.first_name}",
                "Birthday": f"{student.birth_year}-{student.get_month_number()}-{student.birth_day}",
                "StudentID": student.student_id,
                "Seat": student.seat
            })

        with open(f"{self.filename}.json", "w") as file:
            json.dump(data, file)
