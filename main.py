from Console import Console
from Students import Students

students = Students()

# Console
consoleLoop = True
while consoleLoop:
    consoleLoop = Console(students).reader(input())

# Mainframe
