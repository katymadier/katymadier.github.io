# Katy Madier
# Assignment 1
# Due February 12, 2019
# Mac OS 10.13.6

# Assignment Instructions
# Use acoustic tracking to capture some aspect of movement
# 2 page report
# flowchart
# 30 second video
# code & diagrams

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
        self.RATE = 22000
        self.p = pyaudio.PyAudio()
        if startStreaming:
            self.stream_start()

        self.frames = []

        self.listening = True

        #recordings
        self.recording = False
        self.number=0
        self.filename = './audio/audio_' + str(self.number) + '_.wav'
        self.recordedFrames=[]

        #loops
        self.mix = None
        self.numLoops = 0

        #playback
        self.playing = False

         # for tape recording (continuous "tape" of recent audio)
        self.tapeLength=2 #seconds
        self.tape = np.empty(self.RATE*self.tapeLength)*np.nan

        # interactions
        self.tap = False
        self.scrape = False

        AudioSegment.converter = which("ffmpeg")

        # Call the main method to initate the loop:
        self.main()

    def dB(self,a,base=1.0):
        return 10.0*np.log10(a/base)

    def main(self):
        mainloop = True
        while mainloop:
            print('''


                AUDIO LOOPER
                by Katy Madier

                -----------------------------------

                ADDING A NEW SOUND
                    >> TAP >> to start recording 5 seconds of audio
                    s: start

                    >> DOUBLE TAP >>
                    v:

                PLAY THE LOOP
                    >> CLAP >> to start & stop playback
                    p: play
                    p: stop

                    >> QUICK SCRAPE >> to speed up
                    f: fast

                    >> SLOW SCRAPE >> to slow down
                    d: slow

                CLEAR THE LOOP
                    >> BLOW >> to clear the audio
                    c: clear

                QUIT
                    >> PRESS Q or CTRL C >>

                -----------------------------------


            ''')

            key = click.getchar()
            print(key)


            # ADDING A NEW SOUND
            #     >> TAP >> to start & stop recording function
            # s: start
            # s: stop
            if key == 's':
                print('* starting recording, press S to stop...')
                self.start_record()

            #     >> DOUBLE TAP >> to save to the loop
            #     v: save
            if key == 'v':
                print('* saving recording')
                self.save_record()


            # PLAY THE LOOP
            #     >> CLAP >> to start & stop playback
            #     p: play
            #     p: stop
            if key == 'p':
                if self.playing == False:
                    self.replay()
                else:
                    self.playing == True

            #     >> QUICK SCRAPE >> to speed up
            #     f: fast
            #
            #     >> SLOW SCRAPE >> to slow down
            #     d: slow

            # CLEAR THE LOOP
            #     >> BLOW >> to cancel
            #     c: cancel
            if key == 'c':
                print('''
                * recording cancelled. Press:
                 s: to add a new sound to the loop
                 p: to play the loop
                 q: to QUIT
                ''')
                self.stream_stop()

            # QUIT
            #     >> PRESS Q or CTRL C >>
            if key == 'q' or key == 'Q':
                mainloop = False



### OPEN LISTENER TO HEAR FOR BODY INPUT

    def stream_start(self):
        """connect to the audio device and start a stream"""
        print("Audio stream is open and waiting for input")
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1, rate=self.RATE,input=True, frames_per_buffer=self.CHUNK)

    def stream_stop(self):
        """close the stream but keep the PyAudio instance alive."""
        if 'stream' in locals():
            self.stream.stop_stream()
            self.stream.close()
        print(" -- stream CLOSED")

    def close(self):
        """gently detach from things."""
        self.stream_stop()
        self.p.terminate()


### CLASSIFY SOUND
    def categorizingAudio(self):

        fs, data = read(self.filename)
        data_size = len(data)

        #The number of indexes on 0.15 seconds
        focus_size = int(0.15 * fs)

        focuses = []
        idx = 0
        print("Max Frequency", data.max())
        print("Min Frequency", data.min())

        while idx < len(data):

            # checking for taps
            if data[idx]> 4000:
                print(data[idx])
                mean_idx = idx + focus_size // 2
                focuses.append(float(mean_idx) / data_size)
                print("Tap")
                self.tap=True
                idx += focus_size
            else:
                self.tap=False
                # checking for scrapes
                if 2000 <= data[idx]<= 3000:
                        print(data[idx])
                        self.scrape=True
                        mean_idx = idx + focus_size // 2
                        focuses.append(float(mean_idx) / data_size)
                        print("Scrape")
                        idx += focus_size
                else:
                    self.scrape=False
                    idx += 1

    ## TAP
    ## DOUBLE TAP
    ## BLOW
    ## CLAP
    ## QUICK SCRAPE
    ## SLOW SCRAPE

    def stream_read(self):
        """return values for a single chunk"""
        data = np.fromstring(self.stream.read(self.CHUNK, exception_on_overflow = False),dtype=np.int16)
        # print("reading stream", data)
        return data

    # def running_mean(self,x,windowSize):
    #     cumsum = np.cumsum(np.insert(x, 0, 0))
    #     return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize
    #
    # def lowpass(self,cutOffFrequency=1000.0):
    #     print("Running a lowpass filter", self.frames)
    #     audio,duration,frames,bps,dt = self.read_audio(self.frames)
    #     print(audio.shape)
    #
    #     freqRatio = (cutOffFrequency/self.RATE)
    #     N = int(np.sqrt(0.196196 + freqRatio**2)/freqRatio)
    #
    #     # Use moving average.
    #     filtered = self.running_mean(audio, N).astype(audio.dtype)
    #     print(filtered.shape)
    #
    #     # Rewrite to file.
    #     wav_file = wave.open(self.filename + "_lowpass" , "w")
    #     wav_file.setparams((1, bps, self.RATE, frames, 'NONE', 'not compressed'))
    #     wav_file.writeframes(filtered.tobytes('C'))
    #     wav_file.close()



###----------------------
### ADDING A NEW SOUND
    ## IF TAPPED
    ## IF DOUBLE TAPPED
    ## IF BLOW


### tap to start recording/save recording
    def start_record(self):
        print("Started recording a new sound.")
        # setting file name
        try:
            list = sorted(os.listdir('./audio/'))
            file = list[-1]
            print("file", file)
            filestring = file.split('_')
            print("filestring", filestring)
            self.number = int(filestring[1])+ 1
            self.filename = './audio/audio_' + str(self.number) + '_.wav'
        except error as err:
            print("couldn't set filename", error)

        # take stream_read data
        for i in range(0, int(self.RATE / self.CHUNK * int(5))):
            print("recording 5 seconds of audio")
            self.recordedFrames.append(self.stream_read())

        self.save_record()

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

### CLAP to start & stop

    def replay(self):
        if 'mix.wav' in os.listdir():
            while self.playing == True:
                self.numLoops = len(os.listdir('./audio/'))
                print("Playing ", self.numLoops, " audio loops")
                self.mix = AudioSegment.from_wav('mix.wav')
                play(self.mix)

        else:
            print("there is no loop, make one with a tap")



### QUICK SCRAPE to speed up

## SLOW SCRAPE to slow down





### BEGIN PROGRAM
guiAUD = RecAUD()
