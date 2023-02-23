from console.Command.Command import CommandWithArguments
from data.Students import Students


class DelStudent(CommandWithArguments):

    def __init__(self, students: Students):
        self.students = students

    def run(self):
        if not self.hasRequiredArgs(2):
            return

        value = self.args[0]
        type = self.args[1]

        if self.students.isListEmpty():
            self.response.defaultError(f"List is empty")
            return

        if not value.isdigit():
            self.response.defaultError(f"Value is not a digit")
            return

        if not type.isdigit():
            self.response.defaultError(f"Type is not a digit")
            return

        if type == "1":
            if self.students.removeStudentById(int(value)):
                self.response.defaultPrint(f"Student with id {value} deleted")
            else:
                self.response.defaultPrint(f"No student with id {value} found.")

        if type == "2":
            self.students.removeStudentByElement(int(value))
            self.response.defaultPrint(f"Student with index {value} deleted.")