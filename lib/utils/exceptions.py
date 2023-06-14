class AddingStudentError(Exception):
    def __init__(self, message):
        self.message = message

    def print_message(self):
        return self.message


class NoSeatAvailableError(Exception):
    pass


class NoMaxSeatError(Exception):
    pass


class StudentDataStructError(Exception):
    pass


class DuplicateError(Exception):
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
