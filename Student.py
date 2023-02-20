# Mock class atm
class Student:

    def __init__(self, name, birth, id):
        self.name = name
        self.birth = birth
        self.id = id
        self.seat = "NYI"

    def getName(self):
        return self.name

    def getBirth(self):
        return self.birth

    def getId(self):
        return self.id

    def setSeat(self, seat):
        self.seat = seat

    def getSeat(self):
        return self.seat
