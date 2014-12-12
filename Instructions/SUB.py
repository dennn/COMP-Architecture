from Instructions.instruction import Instruction

class SUB(Instruction):

	def __init__(self, currentInstruction):
		self.opcode = currentInstruction.opcode
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 1
		self.instructionType = InstructionType.ALU

	def execute(self):
		self.result = self.decodedOperands[1] - self.decodedOperands[2]

	def writeback(self, processor):
		if self.result == None:
			raise Exception("Result hasn't yet been calculated. Has execute been called?")

		processor.registers[self.destinationRegister] = self.result
