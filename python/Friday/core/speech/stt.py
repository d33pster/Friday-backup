from os.path import join, expanduser
from os import makedirs, unlink

from pydub import AudioSegment
import whisper
import numpy
import speech_recognition
import sounddevice

from Friday.core.exceptions.STTe import NoAudio
from Friday.utils.terminal import Terminal_TEXT_Updater, CLS
from Friday.utils.files import Files

class Command:
    # Configurations
    __RESTING_LABEL = "Friday is online."

    def __init__(self):
        self.__model = whisper.load_model("base")
        self.__recognizer = speech_recognition.Recognizer()
        self.__updater = Terminal_TEXT_Updater()
        self.__listen = Audio()
        self.__screen = CLS()

        self.__files = Files()

        # check dir
        self.__commands_path = join(expanduser('~'), ".friday", "commands")
        makedirs(self.__commands_path, exist_ok=True)
    
    def analyse(self, path_to_audio: str) -> str:
        try:
            return self.__model.transcribe(path_to_audio)["text"]
        except KeyError:
            return ""
    
    def standby(self) -> str:
        # Repeat
        while True:
            # clear the screen
            self.__screen.cls

            # initiate standby until there is audio
            if self.__listen.standby_till_audio(self.__recognizer, self.__updater, self.__RESTING_LABEL, join(self.__commands_path, 'standby.mp3')):
                # if audio is found,
                # analyse
                command = self.analyse(join(self.__commands_path, 'standby.mp3'))
                # remove the audio file
                unlink(join(self.__commands_path, 'standby.mp3'))
                # if there is a command,
                if len(command) > 0:
                    # return command
                    return command
    
    def listen(self) -> str:
        """returns filepath of audio"""
        filename = self.__files.generate_name('command', self.__commands_path)
        self.__listen.listen(join(self.__commands_path, filename))

        return join(self.__commands_path, filename)

class Audio:
    # Configurations
    SAMPLE_RATE = 44100
    CHUNK = 1024
    THRESHOLD = 500

    # __init__
    def __init__(self):
        self.audio: bytes
        self.audio_sample_width: int
        self.if_audio = False
    
    # callback function
    def __callback(self, indata, frames, time, status):
        frames.append(indata.copy())

    def standby_till_audio(self, recogniser_obj: speech_recognition.Recognizer, updater: Terminal_TEXT_Updater, resting_label: str, if_found_save_path: str) -> bool:
        # buffer to hold audio data
        frames = []
        
        # create audio stream
        with sounddevice.InputStream(samplerate=self.SAMPLE_RATE, channels=1, callback=self.__callback):
            updater.message = resting_label
            updater.update
            while True:
                # convert list of frames to numpy array
                audio_data = numpy.concatenate(frames, axis=0)
                frames = []

                # check if there is speech in the audio
                try:
                    audio_segment = speech_recognition.AudioData(audio_data.tobytes(), self.SAMPLE_RATE, 2)
                    recogniser_obj.recognize_whisper(audio_segment)
                    # print(detection_label)
                    # save the audio
                    self.if_audio = True
                    self.audio = audio_data.tobytes()
                    self.audio_sample_width = audio_data.dtype.itemsize
                    self.save(if_found_save_path)
                    return True
                except speech_recognition.UnknownValueError:
                    continue
    
    def listen(self, filename: str, duration: int = 5):
        """listens and automatically saves the file"""
        # record
        audio_data = sounddevice.rec(int(duration * self.SAMPLE_RATE), samplerate=self.SAMPLE_RATE, channels=1, dtype='int16')
        sounddevice.wait()

        # convert np array to AudioSegment
        audio_seg = AudioSegment(
            audio_data.tobytes(),
            frame_rate=self.SAMPLE_RATE,
            sample_width=audio_data.dtype.itemsize,
            channels=1,
        )

        # export
        audio_seg.export(filename, format='mp3')

    
    def save(self, filename_or_filepath: str):
        if self.if_audio:
            audio_seg = AudioSegment(
                self.audio,
                frame_rate=self.SAMPLE_RATE,
                sample_width=self.audio_sample_width,
                channels=1,
            )

            # Export
            audio_seg.export(filename_or_filepath, format='mp3')
        else:
            raise NoAudio("Audio.save cannot be called individually and can only be called from Audio.standby_till_audio!")