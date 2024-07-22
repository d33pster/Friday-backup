# printing management
class Terminal_TEXT_Updater:
    def __init__(self):
        self.__message: str
    
    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value
    
    @message.deleter
    def message(self):
        del self.__message

    @property
    def update(self):
        print(self.message, end="\r")
    
    @property
    def refresh(self):
        self.message = " " * (len(self.message) + 1)
        self.update
    
    @property
    def print(self):
        print(self.message)
        # exit()

# screen management
from platform import system as operating_system
from os import system as run

class CLS:
    def __init__(self):
        self.system = operating_system()
    
    @property
    def cls(self):
        if self.system.lower() == "darwin" or self.system.lower() == "linux":
            run("clear")
        elif self.system.lower() == "windows":
            run("cls")