from Console.Command.Command import CommandStruct
from Console.Command.Commands.AddStudent import AddStudent
from Console.Command.Commands.DelStudent import DelStudent
from Console.Command.Commands.Exit import Exit
from Console.Command.Commands.GetStudents import GetStudents


class GetStudent:
    pass


class AvailableCommands:
    def __init__(self, students):
        self.students = students

    def getCommands(self):
        commands = {
            CommandStruct("AddStudent",
                          "Adds a student to students",
                          "addstudent <name:string> <birthday:string|optional> <matricule:string|optional>",
                          AddStudent(self.students)
                          ),
            CommandStruct("DelStudent",
                          "Deletes a student on either id or index",
                          "delStudent <value:string> <type:1-id, 2-index>",
                          DelStudent(self.students)
                          ),
            CommandStruct("GetStudents",
                          "Shows the current list of students",
                          "getstudents",
                          GetStudents(self.students)
                          ),
            CommandStruct("Exit",
                          "Exits the application",
                          "exit",
                          Exit(self.students)
                          )
        }
        return commands

