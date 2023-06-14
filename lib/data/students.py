import random
import json
import csv

from datetime import datetime
from lib.data.student import Student
from lib.utils.exceptions import NoSeatAvailableError, NoMaxSeatError, StudentDataStructError, DuplicateError
from fpdf import FPDF
from lib.data.dataset import is_student_dict


class Students:

    def __init__(self):
        """
        Constructor.
        """
        self.filename = "default-" + str(datetime.now().strftime("%y%m%d%H%M"))
        self._students_list = list()
        self._seat_list = None
        self._max_seat = None

    # student_list functions
    @property
    def students_list(self) -> list:
        """
        Get the list of students.

        :return: The list of students.
        :rtype: list
        """
        return self._students_list

    @students_list.setter
    def students_list(self, data: dict) -> None:
        """
        Set the list of students.

        :param data: A dictionary containing the student data.
        :type data: dict
        :raises StudentDataStructError: If the dictionary does not meet the required keys.
        :raises DuplicateError: If the data given is a duplicate.
        :raises MaxSeatError: If there is no max seat available
        :raises NoSeatAvailable: If there is no seat available.
        """
        if not is_student_dict(data):
            raise StudentDataStructError()

        if self.is_duplicate(data["student_id"]):
            raise DuplicateError()

        if self.seat_list == -1:
            raise NoMaxSeatError()

        if self.seat_list == 0:
            raise NoSeatAvailableError()

        val = self._seat_list[random.randint(0, self.seat_list - 1)]
        self._seat_list.remove(val)
        data.update({"seat": val})

        self.students_list.append(Student(**data))

    @students_list.deleter
    def students_list(self) -> None:
        """
        Clear the list of students.
        """
        self._students_list.clear()

    def remove_student_by_element(self, e: Student) -> bool:
        """
        Remove a student from the list by the student object.

        :param e: The student object to remove.
        :type e: Student
        :return: True if the student is successfully removed, False otherwise.
        :rtype: bool
        """
        try:
            self._seat_list.append(e.seat)
            self._students_list.remove(e)
            return True
        except ValueError:
            return False

    def remove_student_by_index(self, i: int) -> bool:
        """
        Remove a student from the list by index.

        :param i: The index of the student to remove.
        :type i: int
        :return: True if the student is successfully removed, False otherwise.
        :rtype: bool
        """
        try:
            self._seat_list.append(self._students_list[i])
            self._students_list.pop(i)
            return True
        except IndexError:
            return False

    def remove_student_by_student_id(self, student_id) -> bool:
        """
        Remove a student from the list by student ID.

        :param student_id: The student ID of the student to remove.
        :type student_id: Any
        :return: True if the student is successfully removed, False otherwise.
        :rtype: bool
        """
        for i, x in enumerate(self._students_list):
            if x.student_id == student_id:
                self.remove_student_by_index(i)
                return True

        return False

    def is_duplicate(self, student_id) -> bool:
        """
        Check if a student with the given student ID already exists in the list.

        :param student_id: The student ID to check.
        :type student_id: Any
        :return: True if a duplicate student ID is found, False otherwise.
        :rtype: bool
        """
        for k in self.students_list:
            if k.student_id == student_id:
                return True

        return False

    # seat_list functions
    @property
    def seat_list(self) -> int:
        """
        Get the number of available seats.

        :return: The number of available seats.
        :rtype: int
        """
        if self._seat_list is None:
            return -1

        return len(self._seat_list)

    @seat_list.setter
    def seat_list(self, size: int) -> None:
        """
        Set the number of available seats.

        :param size: The size of the seat list.
        :type size: int
        """
        self._max_seat = size
        self._seat_list = list(range(1, size + 1))

    @seat_list.deleter
    def seat_list(self) -> None:
        """
        Clear the seat list.
        """
        del self.max_seat
        self._seat_list = None

    def is_seat_list(self) -> bool:
        """
        Check if a seat list is available.

        :return: True if a seat list is available, False otherwise.
        :rtype: bool
        """
        return self.seat_list >= 0

    @property
    def max_seat(self) -> int:
        """
        Get the number of maximum seats.

        :return: The number of maximum seats.
        :rtype: int
        """
        if self._max_seat is None:
            return -1
        return self._max_seat

    @max_seat.deleter
    def max_seat(self) -> None:
        """
        Deletes the max_seat
        """
        self._max_seat = None

    # Saving file functions

    def save_as_pdf(self) -> None:
        """
        Save the student data as a PDF file.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.cell(200, 5, txt=f"There are {str(len(self.students_list))} students assigned.", ln=1)
        for i in range(1, self.max_seat+1):
            text = f"{i}. Empty seat"
            for e in self.students_list:
                if e.seat == i:
                    text = f"{i}. ({e.student_id}) {e.last_name} {e.first_name} - {e.birth_day}. {e.birth_month} {e.birth_year}"
            pdf.cell(200, 5, txt=text, ln=1)

        pdf.output(f"{self.filename}.pdf")

    def save_as_csv(self) -> None:
        """
        Save the student data as a CSV file.
        """
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
        """
        Save the student data as a JSON file.
        """
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
