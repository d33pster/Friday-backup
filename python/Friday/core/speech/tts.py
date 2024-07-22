from ...rust import tts

class Reply:
    def __init__(self):
        self.voice = tts.Voice(volume = 3)
    
    def give(self, text: str):
        self.voice.speak(text)
    
    def save(self, text: str, path_to_file: str):
        self.voice.save(text, path_to_file)