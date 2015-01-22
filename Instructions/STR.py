from Instructions.instruction import *

class STR(Instruction):

	def __init__(self, currentInstruction):
		self.listeners = []
		self.opcode = currentInstruction.opcode
		self.rawInstruction = currentInstruction.rawInstruction
		self.operands = currentInstruction.operands
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 4
		self.instructionType = InstructionType.MEMORY
		self.instructionStage = currentInstruction.instructionStage
		self.instructionNumber = currentInstruction.instructionNumber

	def execute(self, processor):
		# Get all the operands
		value = self.decodedOperands[0]
		destination = self.decodedOperands[1]
		
		processor.memory.store(destination, value)

	def writeback(self, processor):
		super(STR, self).writeback(processor)
