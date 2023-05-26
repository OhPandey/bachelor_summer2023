import unittest

from lib.data.students import Students


class TestStudents(unittest.TestCase):
    def setUp(self) -> None:
        self.data = {
            "last_name": "Da Silva Goncalves Joey",
            "first_name": "Joey",
            "birth_day": 3,
            "birth_month": "May",
            "birth_year": 1997,
            "student_id": "0181039342"
        }

        self.data2 = {
            "last_name": "Chiller",
            "first_name": "Kevin",
            "birth_day": 9,
            "birth_month": "February",
            "birth_year": 1991,
            "student_id": "0161032355"
        }

        self.students = Students(10)

    def test_first(self):
        # Testing adding
        self.assertTrue(self.students.add_student(self.data))

        # Testing duplicate
        self.assertFalse(self.students.is_duplicate(self.data2))

    def test_second(self):
        # Testing students list
        self.students.add_student(self.data)
        self.assertEqual(len(self.students.students_list), 1)
        self.students.add_student(self.data2)
        self.assertEqual(len(self.students.students_list), 2)

    def test_third(self):
        self.students.add_student(self.data)
        self.students.add_student(self.data2)

        # Testing removing students
        self.assertTrue(self.students.remove_student_by_student_id(self.data["student_id"]))
        self.assertEqual(len(self.students.students_list), 1)

        self.assertTrue(self.students.remove_student_by_element(self.students.students_list[0]))
        self.assertEqual(len(self.students.students_list), 0)


