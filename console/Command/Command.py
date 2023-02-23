from console.Response.Response import Response


# abstract Command class
class Command:
    response = Response()

    def run(self):
        pass


# abstract CommandWithArguments class
class CommandWithArguments(Command):
    args = list()

    def run(self):
        pass

    def setArgs(self, args):
        self.args = args

    def hasArgs(self):
        if not self.args:
            self.response.missingArgumentWarning()
            return False
        return True

    def hasRequiredArgs(self, number: int):
        if not self.hasArgs():
            return False

        if not len(self.args) == number:
            self.response.missingArgumentWarning()
            return False

        return True


# struct of how a command should look like
class CommandStruct:

    def __init__(self, command: str, desc: str, syntax: str, script: Command):
        self.command = command
        self.desc = desc
        self.syntax = syntax
        self.script = script

    def print(self) -> str:
        return f"{self.command} - {self.desc} | Syntax: {self.syntax}\n"

    def getCommand(self) -> str:
        return self.command

    def getScript(self) -> Command:
        return self.script
