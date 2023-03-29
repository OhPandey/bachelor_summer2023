import random
from console.Command.Command import CommandWithArguments
from lib.Exceptions import InvalidInstanceInListException
from core.student import Student
from core.students import Students


class AddStudent(CommandWithArguments):

    def __init__(self, students: Students):
        self.students = students

    def run(self):
        if not self.hasArgs():
            return

        name = self.args[0]
        birth = ""
        id = random.randint(0, 500000)

        if len(self.args) > 1:
            birth = self.args[1]

        if len(self.args) > 2:
            id = self.args[2]

        try:
            self.students.addStudent(Student(name, birth, id))
            self.response.defaultPrint(f"Student with name = '{name}', birthday = '{birth}', id = '{id}' added")
        except InvalidInstanceInListException as error:
            self.response.internalError(f"{error}. {error.getReason()}")


