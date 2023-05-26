import unittest

from lib.data.student import Student


class TestStudent(unittest.TestCase):
    def test_first(self):
        last_name = "Da Silva Goncalves Joey"
        first_name = "Joey"
        birth_day = 3
        birth_month = "May"
        birth_year = 1997
        student_id = "0181039342"
        seat = 1

        student = Student(last_name, first_name, birth_day, birth_month, birth_year, student_id, seat)

        self.assertEqual(student.get_month_number(), 5)

    def test_second(self):
        last_name = "Chiller"
        first_name = "Kevin"
        birth_day = 9
        birth_month = "February"
        birth_year = 1991
        student_id = "0161032355"
        seat = 1

        student = Student(last_name, first_name, birth_day, birth_month, birth_year, student_id, seat)

        self.assertEqual(student.get_month_number(), 2)

