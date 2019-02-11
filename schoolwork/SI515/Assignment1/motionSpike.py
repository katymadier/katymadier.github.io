# Import the necessary modules.
import pyaudio
import wave
import os
import click
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
#from scipy.signal import butter, lfilter, freqz

# I'm much obliged to user6038351 on stackoverflow for providing framework for much of this code
# (see post here: https://stackoverflow.com/questions/43521804/recording-audio-with-pyaudio-on-a-button-click-and-stop-recording-on-another-but/51229082#51229082)
#
# I'm also much obliged to Dr. Eric Bruning for his insights and code on how to use fft, display audio,
# and answering my general geeky Python questions. See his code here:
# https://gist.github.com/deeplycloudy/2152643


class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=22000, py=pyaudio.PyAudio()):

        # Start Tkinter and set Title
        self.collections = []
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.filename = 'test_recording.wav'

        # Call the main method to initate the loop:
        self.main()

    def dB(self,a,base=1.0):
        return 10.0*np.log10(a/base)


    def main(self,):
        # Start the mainloop, which will be indefinite until 'q' is pressed.
        mainloop = True
        while mainloop:

            print('''

                Press a key to perform that operation...
                f:  get max frequency
                r : record audio and save to file (ctrl+c to stop recording and save)
                p : replay audio file
                d : display the spectrogram of the audio file
                1 : apply simple running-mean low-pass filter to audio signal
                q or Q : quit program

            ''')

            key = click.getchar()
            print(key)

            if key == 'q' or key == 'Q':
                mainloop = False

            if key =='f':
                print('* getting max frequency...')
                self.categorizingAudio()

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

            # if key == '2':
            #     print('* applying highpass filter')
            #     self.highpass()


    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        # somewhat kludgy way to interrupt an active stream, but it works:
        try:
            while self.st == 1:
                data = stream.read(self.CHUNK)
                self.frames.append(data)
                print("* recording")
        except KeyboardInterrupt:
            print('* recording stopped, saved to {}'.format(self.filename))

        stream.close()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    # def stop(self):
    #     self.st = 0

    def replay(self):
        # open the file for reading.
        wf = wave.open(self.filename, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input. These are
        # generic values so that they could technically be used for any wave object,
        # not just the one which was recorded with this selfsame code.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # read data (based on the chunk size)
        data = wf.readframes(self.CHUNK)

        # play stream (looping from beginning of file to the end)
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(self.CHUNK)

        # cleanup stuff.
        stream.close()
        p.terminate()

    def read_audio(self,filename):
        wf = wave.open(self.filename, 'rb')
        nframes = wf.getnframes()
        duration = nframes / float(self.RATE)
        bytes_per_sample = wf.getsampwidth()
        bits_per_sample  = bytes_per_sample * 8
        dtype = 'int{0}'.format(bits_per_sample)
        audio = np.fromstring(wf.readframes(int(duration*self.RATE*bytes_per_sample/self.CHANNELS)), dtype=dtype)

        return audio,duration,nframes,bytes_per_sample,dtype


        # from medium https://medium.com/@almeidneto/sound-pattern-recognition-with-python-9aff69edce5d
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
                idx += focus_size
            else:
                # checking for scrapes
                if 2000 <= data[idx]<= 3000:
                        print(data[idx])
                        mean_idx = idx + focus_size // 2
                        focuses.append(float(mean_idx) / data_size)
                        print("Scrape")
                        idx += focus_size
                else:
                    idx += 1



    # def getfrequency(self):
    #     audio,duration,frames,bps,dt = self.read_audio(self.filename)
    #     fs = self.RATE
    #     audio_fft = np.fft.fft(audio)
    #     freqs = np.fft.fftfreq(audio.shape[0], 1.0/fs) / 1000.0
    #     max_freq_kHz = freqs.max()
    #     print(max_freq_kHz)

    def display(self):
        audio,duration,frames,bps,dt = self.read_audio(self.filename)
        fs = self.RATE
        audio_fft = np.fft.fft(audio)
        freqs = np.fft.fftfreq(audio.shape[0], 1.0/fs) / 1000.0
        max_freq_kHz = freqs.max()
        times = np.arange(audio.shape[0]) / float(fs)
        fftshift = np.fft.fftshift # function saved as variable

        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(8.5,11))
        ax_spec_gram = fig.add_subplot(312)
        ax_fft  = fig.add_subplot(313)
        ax_time = fig.add_subplot(311)
        plt.gcf().subplots_adjust(bottom=0.15)

        ax_spec_gram.specgram(audio, Fs=fs, cmap = 'jet')#cmap='gist_heat')
        ax_spec_gram.set_xlim(0,duration)
        ax_spec_gram.set_ylim(0,max_freq_kHz*1000.0)
        ax_spec_gram.set_ylabel('Frequency (Hz)')
        ax_spec_gram.set_xlabel('Time (s)')

        ax_fft.plot(fftshift(freqs), fftshift(self.dB(audio_fft)))
        ax_fft.set_xlim(0,max_freq_kHz)
        ax_fft.set_xlabel('Frequency (kHz)')
        ax_fft.set_ylabel('dB')

        ax_time.plot(np.arange(frames)/self.RATE,audio/audio.max())
        ax_time.set_xlabel('Time (s)')
        ax_time.set_ylabel('Relative amplitude')
        ax_time.set_xlim(0,duration)

        plt.tight_layout()
        plt.show()

    # from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    # This is similarly referred to a a convolution boxcar filter.
    def running_mean(self,x,windowSize):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

    def lowpass(self,cutOffFrequency=1000.0):
        audio,duration,frames,bps,dt = self.read_audio(self.filename)
        print(audio.shape)

        # Get window size;
        # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        freqRatio = (cutOffFrequency/self.RATE)
        N = int(np.sqrt(0.196196 + freqRatio**2)/freqRatio)

        # Use moving average.
        filtered = self.running_mean(audio, N).astype(audio.dtype)
        print(filtered.shape)

        # Rewrite to file.
        wav_file = wave.open(self.filename, "w")
        wav_file.setparams((1, bps, self.RATE, frames, 'NONE', 'not compressed'))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()

# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()
