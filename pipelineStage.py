class PipelineStage():

	def __init__(self, simulator):
		self.nextInstruction = None
		self.currentInstruction = None
		self.simulator = simulator

	def clockTick(self):
		raise NotImplementedError

	def getNextInstruction(self):
		return self.nextInstruction

