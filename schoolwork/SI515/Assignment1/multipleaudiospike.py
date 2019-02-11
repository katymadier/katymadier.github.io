 # Playing multiple sounds at once from https://stackoverflow.com/questions/39298928/play-multiple-sounds-at-the-same-time-in-python

from pydub import AudioSegment
from pydub.playback import play

audio1 = AudioSegment.from_wav("audio/0452.wav") #your first audio file
audio2 = AudioSegment.from_wav("audio/0999.wav") #your second audio file
audio3 = AudioSegment.from_wav("audio/1160.wav") #your third audio file

mixed = audio1.overlay(audio2)          #combine , superimpose audio files
mixed1  = mixed.overlay(audio3)          #Further combine , superimpose audio files
#If you need to save mixed file
mixed1.export("mixed.wav", format='wav') #export mixed  audio file
# play(mixed)                             #play mixed audio file
