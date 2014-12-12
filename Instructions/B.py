from Instructions.instruction import Instruction

class B(instruction):

	def __init__(self, currentInstruction):
		self.opcode = currentInstruction.opcode
		self.decodedOperands = []
		self.destinationRegister = None
		self.result = None
		self.latency = 1
		self.instructionType = InstructionType.BRANCH

	def execute(self):
		raise Exception("We shouldn't be calling execute on a branch instruction")

	def writeback(self, processor):
		raise Exception("We shouldn't be calling writeback on a branch instruction")

	def willTakeBranch(self, processor):
		processor.pc = self.decodedOperands[0].value.memoryLocation
		return True


