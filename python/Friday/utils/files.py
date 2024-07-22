from os import listdir, getcwd
from os.path import join, expanduser, exists

class Files:
    def __init__(self):
        self.__name: str
    
    def generate_name(self, type: str = "audio", directory: str = getcwd()) -> str:
        self.__name = type + "-001"
        files = listdir(directory)

        while self.__name in files:
            number = str(int(self.__name.split('-')[1]) + 1)
            
            if len(number) < 3:
                number = "0" + number
            
            self.__name = type + "-" + number
        
        return self.__name