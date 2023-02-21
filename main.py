from Console.Command.Commands.AddStudent import AddStudent
from Console.main import Console
from Students import Students

students = Students()

# Console
consoleLoop = True
while consoleLoop:
    consoleLoop = Console(students).reader(input())


# Mainframe
