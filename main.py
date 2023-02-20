from Console import Console
from Student import Student

#AssingSeat Testing

# Set available seats
maxseats = 5

seatList = list(range(0, maxseats))

student1 = Student("Joey", "/", "/")

seatList = student1.assignSeat(seatList, maxseats)

student2 = Student("Joey", "/", "/")

seatList = student2.assignSeat(seatList, maxseats)

student3 = Student("Joey", "/", "/")

seatList = student3.assignSeat(seatList, maxseats)

student4 = Student("Joey", "/", "/")

seatList = student4.assignSeat(seatList, maxseats)

student5 = Student("Joey", "/", "/")

seatList = student5.assignSeat(seatList, maxseats)

print(student1.getSeat())
print(student2.getSeat())
print(student3.getSeat())
print(student4.getSeat())
print(student5.getSeat())


# Console
consoleLoop = True
while consoleLoop:
    consoleLoop = Console().interpreter(input())

# Mainframe
