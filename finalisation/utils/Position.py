class Position:

    adjusted = False

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_width(self):
        return self.x2 - self.x1

    def get_height(self):
        return self.y2 - self.y1

    def add_offset(self, offset):
        self.x1 = self.x1 - offset
        self.y1 = self.y1 - offset
        self.x2 = self.x2 + offset
        self.y2 = self.y2 + offset
        self.adjusted = True
