from console.Command.Command import Command
from data.Students import Students


class GetStudents(Command):

    def __init__(self, students: Students):
        self.students = students

    def run(self):
        if self.students.isListEmpty():
            print("List is empty")
            return
        self.response.defaultPrint(self.students.printStudents())