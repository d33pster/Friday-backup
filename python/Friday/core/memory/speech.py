
from os.path import join, expanduser, exists
from os import makedirs

class What_to_say:
    def __init__(self):
        # define __memory__/what_to_say.txt
        self.memory_path = join(expanduser('~'), ".friday", "__memory__")
        self.say_path = join(self.memory_path, 'what_to_say.txt')

        # define what_to_say = []
        self.what_to_say: list[str] = []
        self.index = 0

        # check if the dir and file exists,
        if exists(self.memory_path) and exists(self.say_path):
            # read what_to_say.txt
            with open(self.say_path, "r+") as wts:
                self.what_to_say = wts.readlines()
            
            # remove "\n"
            for i in range(len(self.what_to_say)):
                self.what_to_say[i] = self.what_to_say[i].replace('\n', '')
        else:
            makedirs(self.memory_path, exist_ok=True)
    
    def add(self, what_to_say: str):
        self.what_to_say.append(what_to_say)
    
    def extend(self, extender: list[str]):
        self.what_to_say.extend(extender)
    
    def add_at_first(self, extendee: list[str]):
        extendee.extend(self.what_to_say)
        self.what_to_say = extendee
    
    @property
    def to_speak(self):
        return self.pointer < self.capacity
    
    @property
    def pointer(self):
        return self.index
    
    @property
    def capacity(self):
        return len(self.what_to_say)
    
    @property
    def say_question_mark(self):
        """what to say next?"""
        try:
            say = self.what_to_say[self.index]
            self.index += 1
            return say
        except IndexError:
            return ""
    
    @property
    def next_time_then(self):
        """save all the stuff u need to say for next time."""
        for i in range(len(self.what_to_say)):
            self.what_to_say[i] += '\n'

        with open(self.say_path, "w+") as wts:
            wts.writelines(self.what_to_say[self.index:])