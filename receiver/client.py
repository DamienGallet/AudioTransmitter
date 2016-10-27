import utilities as util
import record as rec
import protocol as p


class Module:

	def __init__(self):
		self.current_state = p.STATES.NOT_READY

	def make_transition(self):


	def set_ready(self):
		self.current_state = p.STATES.WAITING_INCOMING
