class AddingStudentError(Exception):
    def __init__(self, message):
        self.message = message

    def print_message(self):
        return self.message


class MaxSeatError(Exception):
    pass


class ThreadingError(Exception):
    def __init__(self, message):
        self.message = message

    def print_message(self):
        return self.message


class CameraNotAvailable(Exception):
    pass


class ProcessingNotAvailableError(Exception):
    pass