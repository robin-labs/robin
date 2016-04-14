import pyaudio
import time
import serial

import numpy as np
import matplotlib.pyplot as plt

from scikits.audiolab import *

from config import *
from emit import *
from record import *
from process import *
from util import *
from frames import *

SERIAL_PORT = '/dev/cu.usbmodem14141'
SERIAL_BAUD = 9600

audio = pyaudio.PyAudio()

microphones = choose_input(audio)
print microphones

if microphones is None:
	log_fail("Unable to detect ultramics")

rec = Recorder(audio,input_device_index=microphones.get('index'))
serial = serial.Serial(port=SERIAL_PORT,baudrate=SERIAL_BAUD,write_timeout=0.0)

while True:
	frames = []
	t0 = time.time()
	for i, frame in rec.record(0.15):
		if i == 1:
			serial.write([20,50,5])
			t1 = time.time()
		frames.append(frame)
	us_pulse_start = round(1e6 * (t1 - t0))
	data = frames_to_array(frames)
	left, right = ChannelSample(data[0]), ChannelSample(data[1])
	es = EnvironmentSample([left,right],us_pulse_start)
	if es.process():
		data = es.merge()
		print data
	new_frames = array_to_frames(data)
	play_frames(audio,new_frames,0.05)
