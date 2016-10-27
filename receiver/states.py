import protocol as protocol

class Receiver :

	def __init__(self, module):
		self.received_channels = {}
		for key in protocol.CHANNELS.keys:
			self.received_channels[key] = False

	def received_frequencies(self, frequencies):
		for key in frequencies:
			corresponding_channel = protocol.REVERTED_CHANNELS[key]
			self.received_channels[corresponding_channel] = True
		self.make_transition()



