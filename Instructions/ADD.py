from Instructions.instruction import *

class ADD(Instruction):

	def __init__(self, currentInstruction):
		self.listeners = []
		self.opcode = currentInstruction.opcode
		self.rawInstruction = currentInstruction.rawInstruction
		self.operands = currentInstruction.operands
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 1
		self.instructionType = InstructionType.ALU

	def execute(self, processor):
		self.result = self.decodedOperands[1] + self.decodedOperands[2]

	def writeback(self, processor):
		super(ADD, self).writeback(processor)

		if self.result == None:
			raise Exception("Result hasn't yet been calculated. Has execute been called?")

		processor.registers[self.destinationRegister] = self.result
