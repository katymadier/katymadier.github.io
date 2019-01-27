#Assignment number: 0
#Name: Katy Madier
#Date: 01/13
#Operating system: MacOS High Sierra 10.13.6
#Hardware: Mac Air
#Python Version: Python 3

import pyaudio
import pygame
import aifc
from pynput.keyboard import Key, Listener


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22000
AIFF_OUTPUT_FILENAME = "recording.aiff"
frames = []

p = pyaudio.PyAudio()
af = aifc.open(AIFF_OUTPUT_FILENAME, 'wb')
stream = None

pygame.mixer.init()

#1. Record sound from the external microphones I will give you.
print("* Let's record some audio.")
seconds = input("* How many seconds do you want to record? ")
try:
    print("* Now recording.")
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    for i in range(0, int(RATE / CHUNK * int(seconds))):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("* Recording stopped. You recorded ", seconds, "seconds of audio.")

# 2. Save your recordings to .wav (Windows) or .aiff (Mac) files in mono, with a sampling rate of 22 Khz.
    af.setnchannels(CHANNELS)
    af.setsampwidth(p.get_sample_size(FORMAT))
    af.setframerate(RATE)
    af.writeframes(b''.join(frames))
    af.close()
    print("* Now saving your recording. To play back your recording, press [LEFT SHIFT].")
except:
    print("*** error recording")

#3. Replay the file by pressing a key on your keyboard to start it and stop it.0/
def on_press(key):
    if key == key.shift_l:
        def playRecording():
            try:
                pygame.mixer.music.load(AIFF_OUTPUT_FILENAME)
                pygame.mixer.music.play(-1)
                print("* Playing the recording. To stop playing, press [RIGHT SHIFT].")
            except:
                print("*** error playing audio")
        playRecording()
    if key == key.shift_r:
        def stopPlaying():
            try:
                print("* Stopped playing the recording. To exit this loop press [CONTROL]")
                pygame.mixer.music.stop()
            except:
                print("*** error stopping recording")
        stopPlaying()

    if key == key.ctrl:
        print("Goodbye")
        listener.stop()
        return False

with Listener(
        on_press=on_press) as listener:
    listener.join()


# NOTES
#This listener causes some warning comments from python on a mac. This never interrupted my program... just made it look messy and buried the directions.
# 2019-01-13 18:06:18.120 Python[33092:9043898] pid(33092)/euid(501) is calling TIS/TSM in non-main thread environment, ERROR : This is NOT allowed. Please call TIS/TSM in main thread!!!

# More elegant with pygame... but could never get the key events to register any other keys besides CAPSLOCK....
