"""
----------------------------------------------------------------------
|   This file is responsible for friday's resolve to find out on its |
|   own for when she is needed!                                      |
----------------------------------------------------------------------
                                                                   """

from os.path import join, exists, expanduser
from os import unlink

from Friday.core.speech.tts import Reply
from Friday.core.speech.stt import In

from Friday.core.memory.speech import What_to_say

from Friday.core.commands.list import Clist, Greeting

from Friday.core.soul import Soul

from Friday.utils.terminal import Terminal_TEXT_Updater

class Resolve:
    def __init__(self, speech_memory: What_to_say):
        self.__voicebox = Reply()
        self.__ears = Input()
        self.__speech_mem = speech_memory
        self.__command_handler = Clist(self.__speech_mem)
        self.__clist = self.__command_handler.clist
        self.greeting = Greeting()

        self.updater = Terminal_TEXT_Updater()

        self.__designation = join(expanduser('~'), ".friday", "designation.txt")
    
    @property
    def start(self):
        # check_if_designation_taken = False
        if exists(self.__designation):
            with open(self.__designation, "r+") as d:
                designation = d.read().replace('\n', '')
        else:
            self.__speech_mem.add(f"{Soul().name}.. Starting up!")
            self.__speech_mem.add(f"First time setup initiated! How may I address You?")
            self.reply
            designation = self.__ears.listen
            

    
    @property
    def reply(self):
        while self.__speech_mem.pointer < self.__speech_mem.capacity:
            self.__voicebox.give(self.__speech_mem.say_question_mark)