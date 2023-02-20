# Mock class atm
import random


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

        self.seat = seat+1
        seatlist.remove(seat)
        return seatlist
