from Instructions.instruction import *

class HALT(Instruction):

	def __init__(self, currentInstruction):
		self.opcode = currentInstruction.opcode
		self.rawInstruction = currentInstruction.rawInstruction
		self.operands = []
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 1
		self.instructionType = InstructionType.OTHER

	def execute(self, processor):
		processor.continueRunning = False

	def writeback(self, processor):
		pass
