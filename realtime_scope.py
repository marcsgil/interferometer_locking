#!/usr/bin/python3

from pyfirmata2 import Arduino
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Realtime oscilloscope at a sampling rate of 100Hz
# It displays analog channel 0.
# You can plot multiple chnannels just by instantiating
# more RealtimePlotWindow instances and registering
# callbacks from the other channels.
# Copyright (c) 2018-2020, Bernd Porr <mail@berndporr.me.uk>
# see LICENSE file.

PORT = Arduino.AUTODETECT
# PORT = '/dev/ttyUSB0'

# Creates a scrolling data display


class RealtimePlotWindow:

    def __init__(self, maxlen=500):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        # that's our plotbuffer
        self.buffer = deque(np.zeros(maxlen), maxlen=maxlen)
        # create an empty line
        self.line, = self.ax.plot(self.buffer)
        self.ax.set_ylim(0, 1.01)
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)

    # updates the plot
    def update(self, data):
        self.line.set_ydata(self.buffer)
        return self.line

    # appends data to the ringbuffer
    def addData(self, v):
        self.buffer.append(v)


# Create an instance of an animated scrolling window
# To plot more channels just create more instances and add callback handlers below
realtimePlotWindow = RealtimePlotWindow()

# sampling rate: 100Hz
samplingRate = 100

# called for every new sample which has arrived from the Arduino


def callBack(data):
    # send the sample to the plotwindow
    # add any filtering here:
    # data = self.myfilter.dofilter(data)
    realtimePlotWindow.addData(data)


# Get the Ardunio board.
board = Arduino(PORT)

# Set the sampling rate in the Arduino
board.samplingOn(1000 / samplingRate)

# Register the callback which adds the data to the animated plot
board.analog[1].register_callback(callBack)

# Enable the callback
board.analog[1].enable_reporting()

# show the plot and start the animation
plt.show()

# needs to be called to close the serial port
board.exit()

print("finished")
