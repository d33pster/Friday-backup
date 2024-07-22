
from speech_recognition import Microphone, Recognizer, RequestError, UnknownValueError
from Friday.utils.terminal import Terminal_TEXT_Updater

import sys, os, threading

class STT:
    def __init__(self, wakeup_word: str, resting_label: str, listening_label: str):
        self.Recognizer = Recognizer()
        self.Mic = Microphone()
        self.WAKEUP = wakeup_word
        self.RESTING_LABEL = resting_label
        self.LISTENING_LABEL = listening_label

        self.updater = Terminal_TEXT_Updater()
    
    @property
    def standby(self) -> bool:
        while True:
            with self.Mic as source:
                self.Recognizer.adjust_for_ambient_noise(source, duration=1)
                
                self.updater.refresh
                self.updater.message = " " + self.RESTING_LABEL
                self.updater.update

                audio = self.Recognizer.listen(source, phrase_time_limit=5)

                try:
                    text = self.Recognizer.recognize_vosk(audio).lower()

                    if self.WAKEUP.lower() in text:
                        return True
                    else:
                        continue
                except UnknownValueError:
                    self.updater.refresh
                    self.updater.message = " Err: Unable to understand"
                    self.updater.update
                    continue
                except RequestError as e:
                    self.updater.message = " " + e
                    self.updater.print
                    sys.exit(1)

    def listen(self, phrase_time_limit: int = 1) -> str:
        with self.Mic as source:
            # play beep
            beep_thread = threading.Thread(target=listen_beep_thread_function)
            beep_thread.start()

            self.Recognizer.adjust_for_ambient_noise(source, duration=1)

            beep_thread.join()
            
            self.updater.refresh
            self.updater.message = " " + self.LISTENING_LABEL
            self.updater.update

            try:
                audio = self.Recognizer.listen(source, phrase_time_limit=phrase_time_limit)
            except KeyboardInterrupt:
                sys.exit(0)

            try:
                text = self.Recognizer.recognize_vosk(audio).lower()

                return text
            except UnknownValueError:
                return ""
            except RequestError as e:
                self.updater.message = " " + e + "at listen()"
                self.updater.print
                sys.exit(1)
    
    def process_model_output(self, text: str) -> str:
        return text.split(":")[1].replace("\n", "").replace("}", "").replace("\"", "").strip()

# thread function for listen
def listen_beep_thread_function():
    from pydub import AudioSegment
    from pydub.playback import play

    audio_path = os.path.join(os.path.expanduser('~'), ".friday", "audios")

    audio = AudioSegment.from_wav(os.path.join(audio_path, 'start_rec.wav'))

    play(audio)


