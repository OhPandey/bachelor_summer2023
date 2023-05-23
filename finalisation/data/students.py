import random

from finalisation.data.student import Student
from lib.Exceptions import InvalidInstanceInListException


class Students:
    def __init__(self):
        self.students = list()
        self.seat_list = list(range(10))

    def add_student(self, data):
        if not isinstance(data, dict):
            raise TypeError("Data has to be a dictionary.")

        if "first_name" not in data or "last_name" not in data or "birth_day" not in data or "birth_month" not in data or "birth_year" not in data or "student_id" not in data:
            raise TypeError("Data has a missing key")

        if self.is_duplicate(data["student_id"]):
            raise TypeError("Duplicate")

        if len(self.seat_list) <= 0:
            raise TypeError("No seat available")

        val = self.seat_list[random.randint(0, len(self.seat_list) - 1)]
        self.seat_list.remove(val)

        self.students.append(
            Student(
                first_name=data["first_name"],
                last_name=data["last_name"],
                birth_day=data["birth_day"],
                birth_month=data["birth_month"],
                birth_year=data["birth_year"],
                student_id=data["student_id"],
                seat_list=val
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
