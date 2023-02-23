# This is an interactive console for debugging & analyzing purposes
# It is also used for the final presentation
# It should not be part of the finalized version

from console.Command.AvailableCommands import AvailableCommands
from console.Command.Command import CommandWithArguments
from console.Response.Response import Response


class Console:

    def __init__(self, students):
        self.availableCommands = AvailableCommands(students)
        self.response = Response()
        self.students = students

    def help(self):
        value = ""
        for x in self.availableCommands.getCommands():
            value += x.print()
        self.response.defaultPrint(value)

    def reader(self, string):
        prompt = string.split()
        command = prompt[0]
        prompt.pop(0)
        args = prompt

        if string.upper() == "help".upper():
            self.help()
            return True

        for x in self.availableCommands.getCommands():
            if command.upper() == x.getCommand().upper():
                self.response.defaultGood(f"Command: {command}")
                if isinstance(x.getScript(), CommandWithArguments):
                    x.getScript().setArgs(args)
                x.getScript().run()
                return True

        self.response.defaultWarning(f"Unknown Command: {command}")
        return True
