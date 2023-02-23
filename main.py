from console.main import Console
from data.Students import Students

students = Students()

# Console
consoleLoop = True
while consoleLoop:
    consoleLoop = Console(students).reader(input())


# Mainframe
