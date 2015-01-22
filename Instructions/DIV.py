from Instructions.instruction import *

class DIV(Instruction):

	def __init__(self, currentInstruction):
		self.listeners = []
		self.opcode = currentInstruction.opcode
		self.rawInstruction = currentInstruction.rawInstruction
		self.operands = currentInstruction.operands
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 4
		self.instructionType = InstructionType.ALU
		self.instructionStage = currentInstruction.instructionStage
		self.instructionNumber = currentInstruction.instructionNumber

	def execute(self, processor):
		self.result = self.decodedOperands[1] / self.decodedOperands[2]

	def writeback(self, processor):
		super(DIV, self).writeback(processor)

		if self.result == None:
			raise Exception("Result hasn't yet been calculated. Has execute been called?")

		processor.registers[self.destinationRegister] = self.result
