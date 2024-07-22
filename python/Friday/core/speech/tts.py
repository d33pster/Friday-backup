from ...tts import Voice

class Reply:
    def __init__(self):
        self.voice = Voice(volume = 3)
    
    def give(self, text: str):
        self.voice.speak(text)
    
    def save(self, text: str, path_to_file: str):
        self.voice.save(text, path_to_file)