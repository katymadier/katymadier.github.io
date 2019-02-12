# Katy Madier
# Assignment 1
# Due February 12, 2019
# Mac OS 10.13.6


# Credits
# Much help from https://www.pygame.org/

# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml

# from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean - This is similarly referred to a a convolution boxcar filter.

# Playing multiple sounds at once from https://stackoverflow.com/questions/39298928/play-multiple-sounds-at-the-same-time-in-python

# Setting up an audio listener for open audio stream https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/

# Get window size;
# from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter


try:
    import sys
    import os
    import wave
    import click
    import time
    import numpy as np
    # import matplotlib.pyplot as plt
    import pyaudio
    from scipy.io.wavfile import read
    from pydub import AudioSegment
    from pydub.playback import play
    from pydub.utils import which
except ImportError as err:
    print("couldn't load module.")
    sys.exit(2)

# audio input
class RecAUD:

    def __init__(self, startStreaming=True):
        print("starting up Audio Looper")

        # audio data
        self.collections = []
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.p = pyaudio.PyAudio()
        if startStreaming:
            self.stream_start()

        self.frames = []

        #recordings
        self.number=0
        self.filename ='./audio/audio_' + str("%02d" %  self.number) + '_.wav'
        self.recordedFrames=[]
        self.listeningFrames=[]

        #loops
        self.mix = None
        self.numLoops = 0

        #playback
        self.playing = False

        AudioSegment.converter = which("ffmpeg")

        # Call the main method to initate the loop:
        self.main()

    def dB(self,a,base=1.0):
        return 10.0*np.log10(a/base)

    def main(self):
        mainloop = True
        try:
            while mainloop:
                print('''


                    AUDIO LOOPER
                    by Katy Madier

                    To start/restart listening press S

                    -----------------------------------

                    ADDING A NEW SOUND
                        >> KNOCK >> to start recording 5 seconds of audio

                    PLAY THE LOOP
                        >> TAP >> to start playback

                    QUIT
                        >> PRESS CTRL C >>

                    -----------------------------------


                ''')

                    # [not implemented] >> BLOW >> to remove last recording
                    # [not implemented] >> QUICK SCRAPE >> to speed up
                    # [not implemented] >> SLOW SCRAPE >> to slow down

                key = click.getchar()
                print(key)

                if key == 's' or key == 'S':
                    self.stream_start()

        except KeyboardInterrupt:
            self.stream_stop()
            listening = False
            mainloop = False

### OPEN LISTENER TO HEAR FOR BODY INPUT

    def stream_start(self):
        """connect to the audio device and start a stream"""
        print("Audio stream is open and waiting for you.")
        self.listeningStream=self.p.open(format=pyaudio.paInt16,channels=1, rate=self.RATE,input=True, frames_per_buffer=self.CHUNK)

        self.categorizingAudio()

    def stream_stop(self):
        """close the stream but keep the PyAudio instance alive."""
        if 'stream' in locals():
            listening = False
            self.listeningStream.stop_stream()
            self.listeningStream.close()
            self.recordingStream.stop_stream()
            self.recordingStream.close()
        print("Listening stream has closed. To restart press 's'.")

    def close(self):
        """gently detach from things."""
        self.stream_stop()
        self.p.terminate()


### CLASSIFY SOUND
    def categorizingAudio(self):
        #take open audio and read frames
        try:
            listening = True
            print('Mic is listening for Taps and Knock')
            print('''


                AUDIO LOOPER
                by Katy Madier

                To start/restart listening press S

                -----------------------------------

                ADDING A NEW SOUND
                    >> KNOCK >> to start recording 5 seconds of audio

                PLAY THE LOOP
                    >> TAP >> to start playback

                QUIT
                    >> PRESS CTRL C >>

                -----------------------------------


            ''')
            while listening:
                fs = self.RATE
                data = np.fromstring(self.listeningStream.read(self.CHUNK, exception_on_overflow = False),dtype=np.int16)
                data_size = len(data)
                #The number of indexes on 0.15 seconds
                focus_size = int(0.15 * fs)

                focuses = []
                idx = 0
                # print("Max Frequency", data.max())
                # print("Min Frequency", data.min())

                while idx < len(data):

                    ## KNOCK
                    if data[idx]> 3000:
                        print(data[idx])
                        mean_idx = idx + focus_size // 2
                        focuses.append(float(mean_idx) / data_size)

                        print("someone knocked - now recording audio")
                        self.start_record()

                        idx += focus_size
                        break
                    else:
                        ## TAP
                        if 900 <= data[idx]<= 1100:
                            print(data[idx])
                            mean_idx = idx + focus_size // 2
                            focuses.append(float(mean_idx) / data_size)

                            print("someone tapped - now playing audio")
                            self.replay()

                            idx += focus_size
                            break
                        else:
                            idx += 1

                ## BLOW
                ## DOUBLE TAP
                ## QUICK SCRAPE
                ## SLOW SCRAPE


        except KeyboardInterrupt:
            print('Mic stopped listening to your Taps and Knocks')
            print('''


                AUDIO LOOPER
                by Katy Madier

                To start/restart listening press S

                -----------------------------------

                ADDING A NEW SOUND
                    >> KNOCK >> to start recording 5 seconds of audio

                PLAY THE LOOP
                    >> TAP >> to start playback

                QUIT
                    >> PRESS CTRL C >>

                -----------------------------------


            ''')
            self.stream_stop()


    def stream_read(self):
        """return values for a single chunk"""
        data = np.fromstring(self.recordingStream.read(self.CHUNK, exception_on_overflow = False),dtype=np.int16)
        # print("reading stream", data)
        return data


###----------------------
### ADDING A NEW SOUND

### KNOCK to start recording/save recording
    def start_record(self):
        print("Started recording a new sound.")
        self.recordingStream=self.p.open(format=pyaudio.paInt16,channels=1, rate=self.RATE,input=True, frames_per_buffer=self.CHUNK)
        # setting file name
        try:
            list = sorted(os.listdir('./audio/'))
            file = list[-1]
            # print("file", file)
            if (file != '.DS_Store'):
                filestring = file.split('_')
                # print("filestring", filestring)
                self.number = int(filestring[1])+ 1
                self.filename = './audio/audio_' +  str("%02d" %  self.number) + '_.wav'
            else:
                self.number = 0
                self.filename = './audio/audio_' + str("%02d" %  self.number) + '_.wav'
        except error as err:
            print("couldn't set filename", error)

        # take stream_read data
        self.recordedFrames = []
        for i in range(0, int(self.RATE / self.CHUNK * int(5))):
            self.recordedFrames.append(self.stream_read())
            print("recording 5 seconds of audio")

        self.save_record()
        self.stream_stop()
        self.stream_start()

    def save_record(self):
        print('* recording saved to {}'.format(self.filename))
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.recordedFrames))
        wf.close()
        self.loop_audio()

    def loop_audio(self):
        print("saving to loop")
        ### layer audio files on top and save files
        try:
            for wavefile in os.listdir('./audio/'):
                if (wavefile !='.DS_Store'):
                    # print(wavefile)
                    if 'mix.wav' in os.listdir():
                        # print("there is a mix.wav")
                        mix = AudioSegment.from_wav('mix.wav')
                        audio = AudioSegment.from_wav('./audio/' + wavefile)
                        mixed = mix.overlay(audio, loop=True)
                        mixed.export("mix.wav", format='wav')
                    else:
                        print("no mix.wav")
                        audio = AudioSegment.from_wav('./audio/' + wavefile)
                        audio.export("mix.wav", format='wav')

            self.mix = AudioSegment.from_wav('mix.wav')
            self.numLoops = len(os.listdir('./audio/'))
            print("playing loop")
            print("there are ", self.numLoops, " audio files in this loop")
            play(self.mix)
        except error as err:
            print("couldn't finish audio", error)


###----------------------
### PLAYING THE LOOP

    def replay(self):
        if 'mix.wav' in os.listdir():
            self.numLoops = len(os.listdir('./audio/'))
            print("Playing ", self.numLoops, " audio loops")
            self.mix = AudioSegment.from_wav('mix.wav')
            play(self.mix)
            self.stream_stop()
            self.stream_start()

        else:
            print("there is no loop, record one with a KNOCK")



### QUICK SCRAPE to speed up

## SLOW SCRAPE to slow down





### BEGIN PROGRAM
guiAUD = RecAUD()
