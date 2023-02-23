from lib.Save import Save
from data.Student import *


class Students:

    def __init__(self):
        self.students = list()

    def addStudent(self, student) -> None:
        self.students.append(checkStudent(student))

    def removeStudentByElement(self, e) -> None:
        self.students.pop(e)

    def removeStudentById(self, id) -> bool:
        for i, x in enumerate(self.students):
            if x.getId() == id:
                del self.students[i]
                return True
        return False

    def printStudents(self) -> str:
        text = ""
        for i, x in enumerate(self.students):
            text += f"{i + 1}. {checkStudent(x).print()}\n"
        return text

    def sortByName(self) -> None:
        def sort(e):
            return checkStudent(e).getName()

        self.students.sort(key=sort)

    def sortByBirth(self) -> None:
        def sort(e):
            return checkStudent(e).getBirth()

        self.students.sort(key=sort)

    def sortById(self) -> None:
        def sort(e):
            return checkStudent(e).getId()

        self.students.sort(key=sort)

    def sortBySeat(self) -> None:
        def sort(e):
            e = checkStudent(e)
            # This is a short-handed solution to just not bother with students that are not yet assigned. In a later
            # state it makes sense to use some kind of exception to point that every student has to be assigned
            # somewhere. Alternatively (just came up with the idea) use a global value for max seat?
            # NYI
            if e.getSeat() is None:
                return -1
            return e.getSeat()

        self.students.sort(key=sort)

    def isListEmpty(self) -> bool:
        return True if len(self.students) == 0 else False

    def saveAsPdf(self) -> None:
        Save(self.students).saveAsPdf()
