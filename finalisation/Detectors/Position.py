class Position:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def getX1(self):
        return self.x1

    def getY1(self):
        return self.y1

    def getX2(self):
        return self.x2

    def getY2(self):
        return self.y2

    def getWidth(self):
        return self.x2 - self.x1

    def getHeight(self):
        return self.y2 - self.y1
