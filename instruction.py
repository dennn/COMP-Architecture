class OperandType():
	REGISTER, IMMEDIATE, ADDRESS = range(3)

class Instruction():

	def __init__(self, line):
		self.rawInstruction = line
		self.cleanInstruction()
		self.parseInstruction()

	def cleanInstruction(self):
		self.rawInstruction = [instruction.strip(',') for instruction in self.rawInstruction]
		print self.rawInstruction

	def parseInstruction(self):
		self.opcode = self.rawInstruction[0]
		if self.hasDestinationRegister():
			self.destinationRegister = self.parseRegister(self.rawInstruction[1])
		self.operand1 = self.parseValue(self.rawInstruction[2])

	def parseValue(self, operand):
		if operand[0] == '#':
			return Operand(int(r1[1:]), OperandType.IMMEDIATE)
		elif operand[0] == '[' and r1[-1:] == ']':


	def parseRegister(self, reg):
		newOperand = Operand(int(reg[1:]), OperandType.REGISTER)
		return newOperand

	def hasDestinationRegister(self):
		destinationOpcodes = ["B", "BLT", "BGT", "BEQ", "BNE", "HALT"]
		if self.opcode in destinationOpcodes:
			return False
		else:
			return True

class Operand():

	def __init__(self, value, operandType):
		self.value = value
		self.type = operandType


