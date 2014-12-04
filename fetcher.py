from pipelineStage import PipelineStage

class FetchUnit(PipelineStage):

	def __init__(self, simulator):
		super(FetchUnit, self).__init__(simulator)
		self.program = self.assembledProgram.instructions

	def clockTick(self):
		self.currentInstruction = self.program.instructions[self.simulator.pc]
		self.simulator.pc += 1
		print self.nextInstruction
		self.nextInstruction = self.currentInstruction