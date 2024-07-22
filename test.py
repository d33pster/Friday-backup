#!/usr/bin/env python3
import speech_recognition as sr

WW = "hey siri"

def listen(recognizer: sr.Recognizer, mic: sr.Microphone):
    # recognizer.adjust_for_ambient_noise(mic, duration=1)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("listening..")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_vosk(audio).lower()
            print(f"text: {text}")

            if WW in text:
                print("detected")
                return True
            else:
                return False
        except sr.UnknownValueError:
            print("cannnot understand")
            return False
        except sr.RequestError as e:
            print(f"error: {e}")
            return False

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # recognizer.adjust_for_ambient_noise(mic, duration=1)

    while True:
        if listen(recognizer, mic):
            print("trigger")

main()