# This is an interactive console mainly for debugging & analyzing purposes
# It should not be included in the finalized version

from datetime import datetime


class TextColor:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Command:

    def __init__(self, command, desc, syntax):
        self.command = command
        self.desc = desc
        self.syntax = syntax

    def print(self):
        return f"{self.command} - {self.desc} | {self.syntax}\n"

    def getCommand(self):
        return self.command


def consoleAnswer(color, text):
    if not color:
        print(f"{TextColor.FAIL}[{datetime.now().time()}] Internal Error: TextColor is undefined {TextColor.ENDC}")
    print(f"{color}[{datetime.now().time()}] {text} {TextColor.ENDC}")


class Console:
    commands = {
        Command("Help", "Shows all the available commands", "help"),
        Command("Exit", "Exits the application", "exit")
    }

    def interpreter(self, string):
        arr = string.split()
        command = arr[0]
        arr.pop(0)
        args = arr

        if not self.isCommand(command):
            consoleAnswer(TextColor.WARNING, f"Unknown Command: {command}")
            return True

        if string.upper() == "exit".upper():
            consoleAnswer(TextColor.OKGREEN, "OK")
            return False

        self.runCommands(command, args)
        return True

    def runCommands(self, command, args):
        consoleAnswer(TextColor.OKGREEN, f"Command: {command}")
        command = command.upper()
        if command == "help".upper():
            print(self.getHelp())

    def getHelp(self):
        value = ""
        for x in self.commands:
            value += x.print()
        return value

    def isCommand(self, command):
        for x in self.commands:
            if command.upper() == x.getCommand().upper():
                return True
        return False
