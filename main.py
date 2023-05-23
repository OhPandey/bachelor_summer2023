from finalisation.data.student import Student
from finalisation.data.students import Students

from finalisation.app import App
from finalisation.lib.exceptions import AddingStudentError, MaxSeatError

if __name__ == '__main__':
    # App()
    data = {
            'first_name': 'Joey',
            'last_name': 'DA SILVA GONCALVES',
            'birth_day': '03',
            'birth_month': 'May',
            'birth_year': '1997',
            'student_id': '018109342'
        }
    students = Students()

    print(students.seat_list)
    students.add_student(data)

    print(students.save_as_csv())

