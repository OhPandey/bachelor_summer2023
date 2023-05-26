import unittest

from lib.data.student import Student


class TestStudent(unittest.TestCase):
    def test_init(self):
        last_name = "Da Silva Goncalves Joey"
        first_name = "Joey"
        birth_day = 3
        birth_month = "May"
        birth_year = 1997
        student_id = "0181039342"
        seat = 1

        student = Student(last_name, first_name, birth_day, birth_month, birth_year, student_id, seat)

        self.assertEqual(student.get_month_number(), 5)


if __name__ == '__main__':
    unittest.main()
