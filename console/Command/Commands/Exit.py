from console.Command.Command import Command
from Students import Students


class Exit(Command):

    def __init__(self, students: Students):
        self.students = students

    def run(self):
        self.response.defaultGood("Ending application now")
        self.students.saveAsPdf()
        exit()
