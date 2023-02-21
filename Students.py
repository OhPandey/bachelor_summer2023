from Exceptions import InvalidInstanceInListException
from Student import Student
from Console import TextColor
from Console import consoleAnswer


class Students:

    def __init__(self):
        self.students = list()

    def addStudent(self, student):
        if not isinstance(student, Student):
            raise InvalidInstanceInListException(reason=student)

        self.students.append(student)

    def removeStudentByElement(self, e):
        self.students.pop(e)

    def removeStudentById(self, id):
        for i, x in enumerate(self.students):
            if x.getId() == id:
                del self.students[i]
                return True
        return False

    def printStudents(self):
        text = ""
        for i, x in enumerate(self.students):
            text += f"{i + 1}. {x.print()}\n"
        return text

    # NYI
    def sortById(self):
        return

    def isListEmpty(self):
        return True if len(self.students) == 0 else False

