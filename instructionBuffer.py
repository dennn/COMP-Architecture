import Queue

class InstructionBuffer():

	def __init__(self, program):
		self.buffer = Queue.Queue()
		self.fullProgram = program
		self.fillBuffer()

	def fillBuffer(self):
		for instruction in self.fullProgram:
			self.addInstruction(instruction)

	def addInstruction(self, instruction):
		self.buffer.put(instruction)

	def getNextInstruction(self):
		return self.buffer.get()