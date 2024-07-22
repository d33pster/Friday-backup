"""
----------------------------------------------------------------------
|   This file is responsible for friday's resolve to find out on its |
|   own for when she is needed!                                      |
----------------------------------------------------------------------
                                                                   """

from os.path import join, exists, expanduser
from os import unlink

from Friday.core.speech.tts import Reply
from Friday.core.speech.stt import Command

from Friday.core.memory.speech import What_to_say

from Friday.core.commands.list import Clist, Greeting

from Friday.core.soul import Soul

class Resolve:
    def __init__(self, speech_memory: What_to_say):
        self.__voicebox = Reply()
        self.__ears = Command()
        self.__speech_mem = speech_memory
        self.__command_handler = Clist(self.__speech_mem)
        self.__clist = self.__command_handler.clist
        self.greeting = Greeting()

        self.__designation = join(expanduser('~'), ".friday", "designation.txt")
    
    @property
    def start(self):
        check_if_designation_taken = False
        if exists(self.__designation):
            with open(self.__designation, "r+") as d:
                designation = d.read().replace('\n', '')
        else:
            self.__speech_mem.add(f"{Soul().name}.. Starting up!")
            self.__speech_mem.add(f"First time setup initiated! How may I address You?")
            self.reply
            filepath_to_user_reply = self.__ears.listen()
            designation = self.__ears.analyse(filepath_to_user_reply)
            unlink(filepath_to_user_reply)

            if "sir" in designation.lower():
                designation = "Sir"
            elif "madam" in designation.lower():
                designation = "ma'am"

            with open(self.__designation, "w+") as d:
                d.write(designation)
            
            check_if_designation_taken = True
        
        self.greeting.designation = designation

        if check_if_designation_taken:
            self.__speech_mem.add("Alright!")
            self.reply

        self.standby
    
    @property
    def standby(self):
        # keep checking
        while True:
            # if called
            if "friday" in self.__ears.standby().lower():
                # listen
                filepath = self.__ears.listen()
                # analyse
                analysis = self.__ears.analyse(filepath)

                # delete the filepath
                unlink(filepath)

                # check if it is in commands list
                for command in self.__clist:
                    if command in analysis or analysis in command:
                        # carry out the pathway and register replies
                        self.__command_handler.pathway(self.__clist.index(command)).register
                        break
                
                if self.__speech_mem.to_speak:
                    self.reply

    
    @property
    def reply(self):
        while self.__speech_mem.pointer < self.__speech_mem.capacity:
            self.__voicebox.give(self.__speech_mem.say_question_mark)