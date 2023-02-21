from Exceptions import InvalidInstanceInListException
from Save import Save
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
            if not isinstance(x, Student):
                raise InvalidInstanceInListException(reason=x)
            text += f"{i + 1}. {x.print()}\n"
        return text

    def sortByName(self):
        def sort(e):
            if not isinstance(e, Student):
                raise InvalidInstanceInListException(reason=e)
            return e.getName()

        self.students.sort(key=sort)

    def sortByBirth(self):
        def sort(e):
            if not isinstance(e, Student):
                raise InvalidInstanceInListException(reason=e)
            return e.getBirth()

        self.students.sort(key=sort)

    def sortById(self):
        def sort(e):
            if not isinstance(e, Student):
                raise InvalidInstanceInListException(reason=e)
            return e.getId()

        self.students.sort(key=sort)

    def sortBySeat(self):
        def sort(e):
            if not isinstance(e, Student):
                raise InvalidInstanceInListException(reason=e)
            # This is a short-handed solution to just not bother with students that are not yet assigned. In a later
            # state it makes sense to use some kind of exception to point that every student has to be assigned
            # somewhere. Alternatively (just came up with the idea) use a global value for max seat?
            # NYI
            if e.getSeat() is None:
                return -1
            return e.getSeat()

        self.students.sort(key=sort)

    def isListEmpty(self):
        return True if len(self.students) == 0 else False

    def saveAsPdf(self):
        Save(self.students).saveAsPdf()
