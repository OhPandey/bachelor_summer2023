# This is an interactive console for debugging & analyzing purposes
# It is also used for the final presentation
# It should not be part of the finalized version
import random
from datetime import datetime

from Exceptions import InvalidInstanceInListException
from Student import Student


class TextColor:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Command:

    def __init__(self, command, desc, syntax):
        self.command = command
        self.desc = desc
        self.syntax = syntax

    def print(self):
        return f"{self.command} - {self.desc} | {self.syntax}\n"

    def getCommand(self):
        return self.command


def consoleAnswer(color, text):
    if not color:
        print(f"{TextColor.FAIL}[{datetime.now().time()}] Internal Error: TextColor is undefined {TextColor.ENDC}")
    print(f"{color}[{datetime.now().time()}] {text} {TextColor.ENDC}")


class Console:
    commands = {
        Command("Help", "Shows all the available commands", "help"),
        Command("AddStudent", "Adds a mock student to the studentlists",
                "addstudent <name:string> <birthday:string|optional> <matricule:string|optional>"),
        Command("delStudent", "Deletes a student on either id or index", "delStudent <value:string> <type:1-id, "
                                                                         "2-index>"),
        Command("GetStudents", "Shows the current list of students", "getstudents"),
        Command("Exit", "Exits the application", "exit")
    }

    def __init__(self, students):
        self.students = students

    def interpreter(self, string):

        arr = string.split()
        command = arr[0]
        arr.pop(0)
        args = arr

        if not self.isCommand(command):
            consoleAnswer(TextColor.WARNING, f"Unknown Command: {command}")
            return True

        if string.upper() == "exit".upper():
            consoleAnswer(TextColor.OKGREEN, "OK")
            self.students.saveAsPdf()
            return False

        self.runCommands(command, args)
        return True

    def runCommands(self, command, args):
        consoleAnswer(TextColor.OKGREEN, f"Command: {command}")
        command = command.upper()
        if command == "help".upper():
            print(self.getHelp())

        if command == "addstudent".upper():
            self.addStudent(args)

        if command == "delstudent".upper():
            self.delStudent(args)

        if command == "getstudents".upper():
            print(self.getStudents())

    def getHelp(self):
        value = ""
        for x in self.commands:
            value += x.print()
        return value

    def addStudent(self, args):
        if not args:
            self.errorMissingArguments()
            return

        name = args[0]
        birth = ""
        id = random.randint(0, 500000)
        if len(args) > 1:
            birth = args[1]
        if len(args) > 2:
            id = args[2]

        try:
            self.students.addStudent(Student(name, birth, id))
            print(f"Student with name = '{name}', birthday = '{birth}', id = '{id}' added")
        except InvalidInstanceInListException as error:
            self.errorInternal(f"{error}. {error.getReason()}")

    def delStudent(self, args):
        if not len(args) == 2:
            self.errorMissingArguments()
            return

        value = args[0]
        type = args[1]

        if self.students.isListEmpty():
            consoleAnswer(TextColor.FAIL, f"List is empty")
            return
        if not value.isdigit():
            consoleAnswer(TextColor.FAIL, f"Value is not a digit")
            return
        if not type.isdigit():
            consoleAnswer(TextColor.FAIL, f"Type is not a digit")
            return

        if type == "1":
            if self.students.removeStudentById(int(value)):
                print(f"Student with id {value} deleted.")
            else:
                print(f"No student with id {value} found.")

        if type == "2":
            self.students.removeStudentByElement(int(value))
            print(f"Student with index {value} deleted.")

    def getStudents(self):
        if self.students.isListEmpty():
            return "List is empty"
        return self.students.printStudents()

    def isCommand(self, command):
        for x in self.commands:
            if command.upper() == x.getCommand().upper():
                return True
        return False

    def errorMissingArguments(self):
        consoleAnswer(TextColor.FAIL, f"Missing argument(s), check syntax in help")

    def errorInternal(self, message):
        consoleAnswer(TextColor.FAIL, f"Internal Error: {message}")

