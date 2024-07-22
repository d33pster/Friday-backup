"""
----------------------------------------------------------------------
|   This file is responsible for friday's resolve to find out on its |
|   own for when she is needed!                                      |
----------------------------------------------------------------------
                                                                   """

from os.path import join, exists, expanduser
from os import unlink

from Friday.core.speech.tts import Reply
from Friday.core.speech.stt import STT

from Friday.core.memory.speech import What_to_say

from Friday.core.commands.list import Clist, Greeting

from Friday.core.soul import Soul

from Friday.utils.terminal import Terminal_TEXT_Updater

class Resolve:
    def __init__(self, speech_memory: What_to_say):
        self.__voicebox = Reply()
        self.__ears = STT("friday", "Friday is online.", "Friday is listening..")
        self.__speech_mem = speech_memory
        self.__command_handler = Clist(self.__speech_mem)
        self.__clist = self.__command_handler.clist
        self.greeting = Greeting()

        self.updater = Terminal_TEXT_Updater()

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
            designation = self.__ears.listen(2).lower()

            if "sir" in designation:
                designation = "Sir"
            elif "madam" in designation:
                designation = "Ma'am"
            else:
                designation = self.__ears.process_model_output(designation)
            
            check_if_designation_taken = True
            
        
        print("Designation chosen: " + designation)
        if check_if_designation_taken:
            with open(self.__designation, "w+") as d:
                d.write(designation)
        
        while True:
            # if wake up word
            if self.__ears.standby:
                # listen to command
                command = self.__ears.listen(5).lower()

                # get the actual command
                command = self.__ears.process_model_output(command)
                print("\ncommand:" + command)

                # check the command
                for c in self.__clist:
                    c_ = c.lower().split(" ")
                    check_if_executed = False
                    for x in c_:
                        if x in command:
                            index = self.__clist.index(c)
                            self.__command_handler.designation = designation
                            self.__command_handler.pathway(index).register
                            self.reply
                            check_if_executed = True
                            break
                    
                    if check_if_executed:
                        break

    @property
    def reply(self):
        while self.__speech_mem.pointer < self.__speech_mem.capacity:
            self.__voicebox.give(self.__speech_mem.say_question_mark)