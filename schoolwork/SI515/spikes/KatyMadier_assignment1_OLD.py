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


try:
    import sys
    import random
    import math
    import os
    # import getopt
    # import pygame
    import pyaudio
    import wave
    import click
    import time
    import numpy as np
    import matplotlib.pyplot as plt
    from socket import *
    from pygame.locals import *
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
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        if startStreaming:
            self.stream_start()

        self.frames = []

        # self.st = 1
        # self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        self.number=0
        self.filename = './audio/audio_' + str(self.number) + '_.wav'
        self.mix = None
        self.numLoops = 0
        self.listening = True
         # for tape recording (continuous "tape" of recent audio)
        self.tapeLength=2 #seconds
        self.tape=np.empty(self.rate*self.tapeLength)*np.nan

        AudioSegment.converter = which("ffmpeg")

        # Call the main method to initate the loop:
        self.main()

    def dB(self,a,base=1.0):
        return 10.0*np.log10(a/base)


### OPEN LISTENER TO HEAR FOR BODY INPUT

    def stream_start(self):
        """connect to the audio device and start a stream"""
        print("Audio stream is open and waiting for input")
        self.stream=self.p.open(format=pyaudio.paInt16,channels=1,
                                rate=self.rate,input=True,
                                frames_per_buffer=self.chunk)

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


    ### TAPE METHODS
    # tape is like a circular magnetic ribbon of tape that's continously
    # recorded and recorded over in a loop. self.tape contains this data.
    # the newest data is always at the end. Don't modify data on the type,
    # but rather do math on it (like FFT) as you read from it.

    def tape_add(self):
        """add a single chunk to the tape."""
        self.tape[:-self.chunk]=self.tape[self.chunk:]
        self.tape[-self.chunk:]=self.stream_read()

    def tape_flush(self):
        """completely fill tape with new data."""
        readsInTape=int(self.rate*self.tapeLength/self.chunk)
        print(" -- flushing %d s tape with %dx%.2f ms reads"%\
                  (self.tapeLength,readsInTape,self.chunk/self.rate))
        for i in range(readsInTape):
            self.tape_add()

    def tape_forever(self,plotSec=.25):
        t1=0
        try:
            while True:
                self.tape_add()
                if (time.time()-t1)>plotSec:
                    t1=time.time()
                    # self.tape_plot()
        except:
            print(" ~~ exception (keyboard?)")
            return


    def open_stream(self):
        print("Audio stream is open and waiting for input")
        # start listening
        while (self.listening == True):
            try:
                self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
                data = self.stream.read(self.CHUNK)
                self.frames.append(data)
                print("Listening to data")
                self.classify_sound()

                key = click.getchar()
                print(key)

                if key == 'q' or key == 'Q':
                    self.listening=False

                if key == 'r':
                    print('* starting recording, press ctrl+c to stop...')
                    self.start_record()

                if key == 'p':
                    print('* replaying clip')
                    self.replay()

                if key == 'd':
                    print('* displaying..\n\n')
                    self.display()

                if key == '1':
                    print('* applying lowpass filter')
                    self.lowpass()

                if key == '2':
                    print('* applying highpass filter')
                    self.highpass()

                if key == '3':
                    print('* Create an audio loop')
                    self.loop_audio()


                # stop listening
            except KeyboardInterrupt:
                print('* listening stopped')
                self.listening=False


### CLASSIFY SOUND
    def classify_sound(self):
        print("Classifying input: ")
        self.read_audio()
        # sound.max

    ## TAP
    ## DOUBLE TAP
    ## BLOW
    ## CLAP
    ## QUICK SCRAPE
    ## SLOW SCRAPE
    def stream_read(self):
        """return values for a single chunk"""
        data = np.fromstring(self.stream.read(self.chunk),dtype=np.int16)
        print("reading stream", data)
        return data

    # def read_audio(self,filename):
    #     print("Reading Audio", self.frames)
    #     # wf = wave.open(self.filename, 'rb')
    #     nframes = self.frames
    #     duration = nframes / float(self.RATE)
    #     bytes_per_sample = self.frames.getsampwidth()
    #     bits_per_sample  = bytes_per_sample * 8
    #     dtype = 'int{0}'.format(bits_per_sample)
    #     audio = np.fromstring(self.frames.readframes(int(duration*self.RATE*bytes_per_sample/self.CHANNELS)), dtype=dtype)
    #
    #     return audio,duration,nframes,bytes_per_sample,dtype

    def running_mean(self,x,windowSize):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

    def lowpass(self,cutOffFrequency=1000.0):
        print("Running a lowpass filter", self.frames)
        audio,duration,frames,bps,dt = self.read_audio(self.frames)
        print(audio.shape)

        # Get window size;
        # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        freqRatio = (cutOffFrequency/self.RATE)
        N = int(np.sqrt(0.196196 + freqRatio**2)/freqRatio)

        # Use moving average.
        filtered = self.running_mean(audio, N).astype(audio.dtype)
        print(filtered.shape)

        # Rewrite to file.
        wav_file = wave.open(self.filename + "_lowpass" , "w")
        wav_file.setparams((1, bps, self.RATE, frames, 'NONE', 'not compressed'))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()



###----------------------
### ADDING A NEW SOUND
    ## IF TAPPED
    ## IF DOUBLE TAPPED
    ## IF BLOW


### tap to start recording/save recording
    def start_record(self):
        print("Started recording a new sound.")

        # self.st = 1
        # self.frames = []
        # stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # setting file name
        for wavefile in os.listdir('./audio/'):
            if (wavefile !='.DS_Store'):
                try:
                    filestring = wavefile.split('_')
                    self.number = int(filestring[1]) +1
                    self.filename = './audio/audio_' + str(self.number) + '_.wav'
                except error as err:
                    print("couldn't set filename", error)

        # try:
        #     # start recording
        #     while self.st == 1:
        #         data = self.stream.read(self.CHUNK)
        #         self.frames.append(data)
        #
        #     # stop recording
        # except KeyboardInterrupt:
        #     print('* recording stopped, saved to {}'.format(self.filename))
        #     wf = wave.open(self.filename, 'wb')
        #     wf.setnchannels(self.CHANNELS)
        #     wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        #     wf.setframerate(self.RATE)
        #     wf.writeframes(b''.join(self.frames))
        #     wf.close()


        # try:
        #     # start recording
        #     while self.st == 1:
        #         data = self.stream.read(self.CHUNK)
        #         self.frames.append(data)
        #         print("* recording")
        # # stop recording & saving file
        # except KeyboardInterrupt:
        #     print('* recording stopped, saved to {}'.format(self.filename))
        #     wf = wave.open(self.filename, 'wb')
        #     wf.setnchannels(self.CHANNELS)
        #     wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        #     wf.setframerate(self.RATE)
        #     wf.writeframes(b''.join(self.frames))
        #     wf.close()
        #     # stream.close()

    def loop_audio(self):
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
            play(self.mix)
        except error as err:
            print("couldn't finish audio", error)


    # def display(self):
    #     audio,duration,frames,bps,dt = self.read_audio(self.filename)
    #     fs = self.RATE
    #     audio_fft = np.fft.fft(audio)
    #     freqs = np.fft.fftfreq(audio.shape[0], 1.0/fs) / 1000.0
    #     max_freq_kHz = freqs.max()
    #     times = np.arange(audio.shape[0]) / float(fs)
    #     fftshift = np.fft.fftshift # function saved as variable
    #
    #     import matplotlib.pyplot as plt
    #     fig = plt.figure(figsize=(8.5,11))
    #     ax_spec_gram = fig.add_subplot(312)
    #     ax_fft  = fig.add_subplot(313)
    #     ax_time = fig.add_subplot(311)
    #     plt.gcf().subplots_adjust(bottom=0.15)
    #
    #     ax_spec_gram.specgram(audio, Fs=fs, cmap = 'jet')#cmap='gist_heat')
    #     ax_spec_gram.set_xlim(0,duration)
    #     ax_spec_gram.set_ylim(0,max_freq_kHz*1000.0)
    #     ax_spec_gram.set_ylabel('Frequency (Hz)')
    #     ax_spec_gram.set_xlabel('Time (s)')
    #
    #     ax_fft.plot(fftshift(freqs), fftshift(self.dB(audio_fft)))
    #     ax_fft.set_xlim(0,max_freq_kHz)
    #     ax_fft.set_xlabel('Frequency (kHz)')
    #     ax_fft.set_ylabel('dB')
    #
    #     ax_time.plot(np.arange(frames)/self.RATE,audio/audio.max())
    #     ax_time.set_xlabel('Time (s)')
    #     ax_time.set_ylabel('Relative amplitude')
    #     ax_time.set_xlim(0,duration)
    #
    #     plt.tight_layout()
    #     plt.show()

###----------------------
### PLAYING THE LOOP

### CLAP to start & stop

    def replay(self):
        if 'mix.wav' in os.listdir():
            self.numLoops = len(os.listdir('./audio/'))
            print("Playing ", self.numLoops, " audio loops")
            self.mix = AudioSegment.from_wav('mix.wav')
            play(self.mix)
        else:
            print("there is no loop, make one with a tap")

    def stop(self):
        self.st = 0


### QUICK SCRAPE to speed up

## SLOW SCRAPE to slow down



    def main(self):
        print('''


            AUDIO LOOPER
            by Katy Madier

            -----------------------------------

            ADDING A NEW SOUND
                >> TAP >> to start & stop recording function
                >> DOUBLE TAP >> to save to the loop
                >> BLOW >> to cancel

            PLAY THE LOOP
                >> CLAP >> to start & stop playback
                >> QUICK SCRAPE >> to speed up
                >> SLOW SCRAPE >> to slow down

            -----------------------------------


            Press a key to perform that operation...
            r : record audio and save to file (ctrl+c to stop recording and save)

            d : display the spectrogram of the audio file
            1 : apply simple running-mean low-pass filter to audio signal
            2 : apply highpass filter
            3 : create an audio loop
            q or Q : quit program

        ''')

        ### OPEN LISTENER TO HEAR FOR BODY INPUT

        # ### ADDING A NEW SOUND
        # ## IF TAPPED
        # self.start_record()
        # #stop
        #
        # ## IF DOUBLE TAPPED
        # self.loop_audio()
        #
        # ## IF BLOW
        #     #erase
        #
        # ### PLAY THE LOOP
        # ## IF CLAP
        # self.replay()
        # #stop
        #
        # ## IF QUICK SCRAPE
        # ## IF SLOW SCRAPE





### BEGIN PROGRAM
guiAUD = RecAUD()
