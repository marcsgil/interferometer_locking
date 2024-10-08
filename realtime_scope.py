#!/usr/bin/python3

from pyfirmata2 import Arduino
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time
from numpy.fft import fft, fftfreq

# Realtime oscilloscope at a sampling rate of 100Hz
# It displays analog channel 0.
# You can plot multiple chnannels just by instantiating
# more RealtimePlotWindow instances and registering
# callbacks from the other channels.
# Copyright (c) 2018-2020, Bernd Porr <mail@berndporr.me.uk>
# see LICENSE file.

PORT = Arduino.AUTODETECT
# PORT = '/dev/ttyUSB0'

# sampling rate: 100Hz
samplingRate = 1000

t0 = time()
sine_freq = 90
freq = np.linspace(0,99.8, 250)

# Creates a scrolling data display
class RealtimePlotWindow:

    def __init__(self):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        # that's our plotbuffer
        self.plotbuffer = np.zeros(500)
        # create an empty line
        self.line, = self.ax.plot(freq, self.plotbuffer[:250])
        # axis
        self.ax.set_ylim(0, 60)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # add any initialisation code here (filters etc)
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)

    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(np.abs(fft(self.plotbuffer)[:250]))
        return self.line,

    # appends data to the ringbuffer
    def addData(self, v):
        self.ringbuffer.append(v)


# Create an instance of an animated scrolling window
# To plot more channels just create more instances and add callback handlers below
realtimePlotWindow = RealtimePlotWindow()



# called for every new sample which has arrived from the Arduino
def callBack(data):
    # send the sample to the plotwindow
    # add any filtering here:
    # data = self.myfilter.dofilter(data)
    realtimePlotWindow.addData(data)
    v = np.sin(2 * np.pi * sine_freq * (time()-t0))
    pwm_5.write(0.5 + 0.5 * v)

# Get the Ardunio board.
board = Arduino(PORT)

pwm_5 = board.get_pin('d:5:p')

# Set the sampling rate in the Arduino
board.samplingOn(1000 / samplingRate)

# Register the callback which adds the data to the animated plot
board.analog[0].register_callback(callBack)

# Enable the callback
board.analog[0].enable_reporting()

# show the plot and start the animation
plt.show()

# needs to be called to close the serial port
board.exit()

print("finished")
