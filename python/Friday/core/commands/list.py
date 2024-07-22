
from datetime import datetime

from Friday.core.memory.speech import What_to_say
from Friday.core.soul import Soul

class Greeting:
    def __init__(self):
        self._greeting = ""
        self._designation = "Sir"
    
    @property
    def greeting(self):
        hour = int(datetime.now().hour)

        if hour >= 0 and hour < 12:
            self.greeting = f"Good Morning {self.designation}!"
        elif hour >= 12 and hour < 18:
            self.greeting = f"Good Afternoon {self.designation}!"
        else:
            self.greeting = f"Good Evening {self.designation}!"
        
        return self._greeting
    
    @greeting.setter
    def greeting(self, value: str):
        self._greeting = value
    
    @property
    def designation(self):
        return self._designation
    
    @designation.setter
    def designation(self, value: str):
        self._designation = value

class PathwayData:
    def __init__(self, memory: What_to_say, to_register: list[str]):
        self.mem = memory
        self.to_register = to_register
    
    @property
    def register(self):
        self.mem.extend(self.to_register)

class Clist:
    def __init__(self, speech_memory: What_to_say):
        self.speech_mem = speech_memory
        self._designation = "Sir"

        self.__clist__ = [
            "Friday",
        ]
    
    @property
    def clist(self):
        return self.__clist__

    @property
    def designation(self):
        return self._designation
    
    @designation.setter
    def designation(self, value: str):
        self._designation = value
    
    def pathway(self, clist_index: int) -> PathwayData:
        command = self.__clist__[clist_index]

        if command == "Friday":
            greeting = Greeting()
            greeting.designation = self.designation

            to_register = [
                greeting.greeting,
                f"{Soul().name}... {Soul().version_in_words}, At your Service!"
            ]
        
        return PathwayData(self.speech_mem, to_register=to_register)
