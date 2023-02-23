# Mock class atm
import random

from lib.Exceptions import InvalidInstanceInListException


class Student:

    def __init__(self, name, birth, id):
        self.name = name
        self.birth = birth
        self.id = id
        self.seat = None

    def getName(self):
        return self.name

    def getBirth(self):
        return self.birth

    def getId(self):
        return self.id

    def getSeat(self):
        return self.seat

    def assignSeat(self, seatlist, maxseat):
        # Get a random seatnumber
        seat = random.randint(0, maxseat - 1)

        # Reroll if its already used
        while seat not in seatlist:
            seat = random.randint(0, maxseat - 1)

        self.seat = seat + 1
        seatlist.remove(seat)
        return seatlist

    def print(self):
        return f"Name: '{self.name}', Birthday: '{self.birth}', id: '{self.id}'"


def checkStudent(student) -> Student:
    if not isinstance(student, Student):
        raise InvalidInstanceInListException(reason=student)
    return student
