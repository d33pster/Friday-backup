class Soul:
    def __init__(self):
        self.__name = "Friday"
        self.__version = "1.0"
        self.__version_in_words = "one point O"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def version(self) -> str:
        return self.__version

    @property
    def version_in_words(self) -> str:
        return self.__version_in_words