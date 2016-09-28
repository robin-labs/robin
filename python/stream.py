import sounddevice as sd
import numpy as np

def create_stream(settings, device, output, callback, **kwargs):
	Stream = sd.OutputStream if output else sd.InputStream
	return Stream(
		samplerate=settings.rate,
		blocksize=settings.chunk,
		device=device.index,
		channels=settings.channels,
		dtype=settings.np_format,
		callback=callback,
		**kwargs
	)

def transposed(sample):
	return np.transpose(sample)

class SampleBuffer(object):
	def __init__(self):
		self.queue = []

	def put(self, sample):
		self.queue.append(np.copy(sample))

	def has(self):
		return len(self.queue) > 0

	def get_chunk(self):
		return self.queue.pop(0)

	def get_samples(self, length, channels):
		pointer = 0
		buff = np.zeros((channels, length))
		while pointer < length:
			if not len(self.queue):
				break
			else:
				sample = self.queue[0]
				sample_length = sample.shape[1]
				take = min(length - pointer, sample_length)
				buff[:, pointer : pointer + take] = sample[:, 0:take]
				self.queue[0] = sample[:, take:]
				pointer = pointer + take
				if not self.queue[0].shape[1]:
					self.queue.pop(0)
		return buff
