import pyfirmata2
from time import sleep
import numpy as np

# PWM demo on port 5. The default PWM frequency is 1kHz.

# Adjust that the port match your system, see samples below:
# On Linux: /dev/tty.usbserial-A6008rIF, /dev/ttyACM0,
# On Windows: \\.\COM1, \\.\COM2
# PORT = '/dev/ttyACM0'
PORT = pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT)
print("Setting up the connection to the board ...")

# Setup the digital pin for PWM
pwm_5 = board.get_pin('d:5:p')

sine_freq = 50
write_interval = 0.001

t = 0

while True:
    v = np.sin(2 * np.pi * sine_freq * t)
    pwm_5.write(0.9 + 0.1 * v)
    t += write_interval
    sleep(write_interval)
