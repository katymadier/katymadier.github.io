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

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import pyaudio
    import wave
    import click
    import numpy as np
    import matplotlib.pyplot as plt
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module.")
    sys.exit(2)

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()

# audio input
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

# categorize audio data for type of sound
### detect Frequency
    # def detect(self):



### snap to select item through list
    # def select()

### tap to start recording/save recording
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

    def read_audio(self,filename):
        wf = wave.open(self.filename, 'rb')
        nframes = wf.getnframes()
        duration = nframes / float(self.RATE)
        bytes_per_sample = wf.getsampwidth()
        bits_per_sample  = bytes_per_sample * 8
        dtype = 'int{0}'.format(bits_per_sample)
        audio = np.fromstring(wf.readframes(int(duration*self.RATE*bytes_per_sample/self.CHANNELS)), dtype=dtype)

        return audio,duration,nframes,bytes_per_sample,dtype

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

    def replay(self):
        # open the file for reading.
        wf = wave.open(self.filename, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input. These are generic values so that they could technically be used for any wave object, not just the one which was recorded with this selfsame code.
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

### scratch to erase recording
    # def erase()

### blow to play/stop
    def stop(self):
        self.st = 0




# the music looper

    def main(self):
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((640, 580))
        pygame.display.set_caption('Sound Looper')

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((251,225,63))

        # Audio blocks
        block1 = pygame.draw.rect(background,(0,0,0), (20,20,600,100))
        block1Text = pygame.font.Font(None,40)
        textRender = block1Text.render("1", True, [255, 255, 255], [255, 255, 255])

        block2= pygame.draw.rect(background,(0,0,0), (20,140,600,100))
        block3 = pygame.draw.rect(background,(0,0,0), (20,260,600,100))
        block4 = pygame.draw.rect(background,(0,0,0), (20,380,600,100))

        #buttons
        button1 = pygame.draw.circle(background, (0,0,0), (60, 530), 40)

        # # Initialise players
        # global player1
        # global player2
        # player1 = Bat("left")
        # player2 = Bat("right")

        # # Initialise ball
        # speed = 13
        # rand = ((0.1 * (random.randint(5,8))))
        # ball = Ball((0,0),(0.47,speed))

        # Initialise sprites
        # playersprites = pygame.sprite.RenderPlain((player1))
        # ballsprite = pygame.sprite.RenderPlain(ball)

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        # pygame.display.flip()

        # Initialise clock
        clock = pygame.time.Clock()

        # Event loop
        while 1:
            # Make sure game doesn't run at more than 60 frames per second
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                # elif event.type == KEYDOWN:
                #     if event.key == K_a:
                #         start_record(self)
                # #     #     player1.moveup()
                #     if event.key == K_z:
                #         read_audio(self,filename)
                # #     #     player1.movedown()
                #     if event.key == K_UP:
                #         replay(self)
                #     #     player2.moveup()
                #     # if event.key == K_DOWN:
                #     #     player2.movedown()
                # elif event.type == KEYUP:
                #     # if event.key == K_a or event.key == K_z:
                #     #     player1.movepos = [0,0]
                #     #     player1.state = "still"
                #     # if event.key == K_UP or event.key == K_DOWN:
                #     #     player2.movepos = [0,0]
                #     #     player2.state = "still"

            # screen.blit(background, ball.rect, ball.rect)
            # screen.blit(background, player1.rect, player1.rect)
            # screen.blit(background, player2.rect, player2.rect)
            # ballsprite.update()
            # playersprites.update()
            # ballsprite.draw(screen)
            # playersprites.draw(screen)
            # Start the mainloop, which will be indefinite until 'q' is pressed.

            print('''

                Press a key to perform that operation...
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

            pygame.display.flip()

# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()

# if __name__ == '__main__': main()


# class Ball(pygame.sprite.Sprite):
#     """A ball that will move across the screen
#     Returns: ball object
#     Functions: update, calcnewpos
#     Attributes: area, vector"""
#
#     def __init__(self, xy, vector):
#         pygame.sprite.Sprite.__init__(self)
#         self.image, self.rect = load_png('ball.png')
#         screen = pygame.display.get_surface()
#         self.area = screen.get_rect()
#         self.vector = vector
#         self.hit = 0
#
#     def update(self):
#         newpos = self.calcnewpos(self.rect,self.vector)
#         self.rect = newpos
#         (angle,z) = self.vector
#
#         if not self.area.contains(newpos):
#             tl = not self.area.collidepoint(newpos.topleft)
#             tr = not self.area.collidepoint(newpos.topright)
#             bl = not self.area.collidepoint(newpos.bottomleft)
#             br = not self.area.collidepoint(newpos.bottomright)
#             if tr and tl or (br and bl):
#                 angle = -angle
#             if tl and bl:
#                 #self.offcourt()
#                 angle = math.pi - angle
#             if tr and br:
#                 angle = math.pi - angle
#                 #self.offcourt()
#         else:
#             # Deflate the rectangles so you can't catch a ball behind the bat
#             player1.rect.inflate(-3, -3)
#             player2.rect.inflate(-3, -3)
#
#             # Do ball and bat collide?
#             # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
#             # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
#             # bat, the ball reverses, and is still inside the bat, so bounces around inside.
#             # This way, the ball can always escape and bounce away cleanly
#             if self.rect.colliderect(player1.rect) == 1 and not self.hit:
#                 angle = math.pi - angle
#                 self.hit = not self.hit
#             elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
#                 angle = math.pi - angle
#                 self.hit = not self.hit
#             elif self.hit:
#                 self.hit = not self.hit
#         self.vector = (angle,z)
#
#     def calcnewpos(self,rect,vector):
#         (angle,z) = vector
#         (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
#         return rect.move(dx,dy)
#
# class Bat(pygame.sprite.Sprite):
#     """Movable tennis 'bat' with which one hits the ball
#     Returns: bat object
#     Functions: reinit, update, moveup, movedown
#     Attributes: which, speed"""
#
#     def __init__(self, side):
#         pygame.sprite.Sprite.__init__(self)
#         self.image, self.rect = load_png('bat.png')
#         screen = pygame.display.get_surface()
#         self.area = screen.get_rect()
#         self.side = side
#         self.speed = 10
#         self.state = "still"
#         self.reinit()
#
#     def reinit(self):
#         self.state = "still"
#         self.movepos = [0,0]
#         if self.side == "left":
#             self.rect.midleft = self.area.midleft
#         elif self.side == "right":
#             self.rect.midright = self.area.midright
#
#     def update(self):
#         newpos = self.rect.move(self.movepos)
#         if self.area.contains(newpos):
#             self.rect = newpos
#         pygame.event.pump()
#
#     def moveup(self):
#         self.movepos[1] = self.movepos[1] - (self.speed)
#         self.state = "moveup"
#
#     def movedown(self):
#         self.movepos[1] = self.movepos[1] + (self.speed)
#         self.state = "movedown"
