from Instructions.instruction import *

class LDR(Instruction):

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

	def execute(self, processor):
		# Get all the operands
		operand1 = self.decodedOperands[1]
		
		# Is it a memory type of operation
		if self.operands[1].memoryLookup == True:
			self.result = processor.memory.load(operand1)
		else:
			if self.operands[1].type == OperandType.REGISTER:
				self.result = processor.registers[operand1]
			elif self.operands[1].type == OperandType.IMMEDIATE:
				self.result = operand1

	def writeback(self, processor):
		if self.result == None:
			raise Exception("Result hasn't yet been calculated. Has execute been called?")

		processor.registers[self.destinationRegister] = self.result

		super(LDR, self).writeback(processor)
