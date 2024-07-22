
from Friday.core.flow.resolve import Resolve
from Friday.core.memory.speech import What_to_say

def main():
    # set memory
    memory = What_to_say()

    # define resolve
    resolve = Resolve(speech_memory=memory)

    resolve.start