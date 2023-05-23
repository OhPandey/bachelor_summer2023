from finalisation.data.student import Student
from finalisation.data.students import Students

from finalisation.app import App

if __name__ == '__main__':
    # App()
    data = {
            'first_name': 'DA SILVA GONCALVES',
            'last_name': 'Joey',
            'birth_day': '03',
            'birth_month': 'May',
            'birth_year': '1997',
            'student_id': '018109342'
        }
    students = Students()
    print(students.seat_list)
    students.add_student(data)

    print(students.seat_list)
    students.add_student(data)
    print(students.seat_list)
    print(len(students.students))

