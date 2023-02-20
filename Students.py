from Student import Student
from Console import TextColor
from Console import consoleAnswer


class Students:

    def __init__(self):
        self.students = list()

    def addStudent(self, student):
        if isinstance(student, Student):
            self.students.append(student)
        else:
            consoleAnswer(TextColor.FAIL, "Internal Error: Impossible to assign Student as student is not part of "
                                          "student class")

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

    def isListEmpty(self):
        return True if len(self.students) == 0 else False
