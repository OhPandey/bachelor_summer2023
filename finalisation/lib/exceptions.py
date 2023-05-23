class AddingStudentError(Exception):
    def __init__(self, message):
        self.message = message

    def print_message(self):
        return self.message


class MaxSeatError(Exception):
    pass
