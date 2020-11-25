# Karplus-Strong algorithm

import numpy as np
from matplotlib import pyplot as plt
import pygame
import wave
import math
from collections import deque
import random
import argparse
import os
import sys
import time


# sRate = 44100
# nSample = sRate*5
# x = np.arrange(nSample)/float(sRate)
# vals = np.sin(2.0 * math.pi * 220.0 * x)
# data = np.array(vals*32767, 'int16').tostring()
# file = wave.open('sine220.wav', 'wb')
# file.setparams((1, 2, sRate, nSample, 'NONE', 'uncompressed'))
# file.writeframes(data)
# file.close()
# show plot of algorithm in action
gShowPlot = False

# notes of a Pentatonic Minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}


# write a WAV File
def writeWAVE(fname, data):
    # open file
    file = wave.open(fname, 'wb')
    # WAV file parameters
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    # set parameters
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()


# generate note of given frequency
def generateNote(freq):
    nSample = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    # initialise ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    # initialise sample buffer
    samples = np.array([0]*nSample, 'float32')
    for i in range(nSample):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()
        # plot of flag set
        if gShowPlot:
            if 1 % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()

    # convert samples to 16-bit values and then to a string
    # the max value is 32767 for 16-bit
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()


# playing WAV Files with pygame
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # dictionary of notes
        self.notes = {}
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print('{} not found!'.format(fileName))
    def playRandom(self):
        """play a random note"""
        index = random.randint(0, len(self.notes)-1)

        note = list(self.notes.values())[index]
        note.play()

def main():
    parser = argparse.ArgumentParser(description='Generating sounds with Karplus-Strong Algorithm')
    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)
    args = parser.parse_args()

    # show plot of flag set
    if args.display:
        gShowPlot = True
        plt.ion()

    # create note player
    nplayer = NotePlayer()

    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print('Creating {}...'.format(fileName))
            writeWAVE(fileName, data)
        else:
            print('{} already created, skipping...'.format(fileName))

        # add note to player
        nplayer.add(name + '.wav')


        # play note if display flag set
        if args.display:
            nplayer.play(name + '.wav')
            time.sleep(0.5)

    # play a random tune
    if args.play:
        while True:
            try:
                nplayer.playRandom()
                # rest - 1 to 8 beats
                rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()

    # random piano mode
    if args.piano:
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYUP):
                    print('key pressed')
                    nplayer.playRandom()
                    time.sleep(0.5)

if __name__ == '__main__':
    main()

