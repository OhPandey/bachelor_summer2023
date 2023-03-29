class InvalidInstanceInListException(Exception):
    # Exception raised when trying to add a non-student core to the students list
    def __init__(self, message="Element of the students list is not part of the Student core", reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        return str(self.message)

    # Optional Exception message
    def getReason(self):
        return "No reason found" if self.reason is None else "Reason: " + str(self.reason)
