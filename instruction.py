class OperandType():
	REGISTER, IMMEDIATE, LABEL = range(3)

class Instruction():

	def __init__(self, line, assembler):
		self.rawInstruction = line
		self.operands = []
		self.decodedOperands = []
		self.destinationRegister = None
		self.opcode = None
		self.assembler = assembler
		self.parseInstruction()
		self.latency = 1
		self.result = None

	def __str__(self):
		return ' '.join(self.rawInstruction)

	def parseInstruction(self):
		self.opcode = self.rawInstruction[0]
		self.setLatency()
		for operand in self.rawInstruction[1:]:
			self.operands.append(self.parseValue(operand))

	def setLatency(self):
		opcode = self.opcode

		if opcode == 'LDR':
			self.latency = 1
		elif opcode == 'STR':
			self.latency = 1
		elif opcode == 'ADD':
			self.latency = 1
		elif opcode == 'SUB':
			self.latency = 1
		elif opcode == 'B':
			self.latency = 1
		elif opcode == 'BNE':
			self.latency = 1
		elif opcode == 'BEQ':
			self.latency = 1
		elif opcode == 'BLT':
			self.latency = 1
		elif opcode == 'BGT':
			self.latency = 1
		elif opcode == 'HALT':
			self.latency = 1

	def parseValue(self, operand):
		# First check if it's a label
		labelLookup = self.assembler.labelLookup(operand)
		if labelLookup != None:
			return Operand(labelLookup, OperandType.LABEL, True)
		# Then immediate
		elif operand[0] == '#':
			return Operand(int(operand[1:]), OperandType.IMMEDIATE, False)
		# Then address
		elif operand[0] == '[' and operand[-1:] == ']':
			return self.parseAddress(operand)
		# Then register
		else:
			return self.parseRegister(operand)

	def parseRegister(self, reg):
		if reg[0].upper() != 'R':
			raise Exception("Invalid syntax in instruction: " + reg)
		newOperand = Operand(int(reg[1:]), OperandType.REGISTER, False)
		return newOperand

	def parseAddress(self, address):
		address = address.replace(',', '')
		address = address.replace(']', '')
		address = address.replace('[', '')

		# First check if it's a label
		labelLookup = self.assembler.labelLookup(address)
		if labelLookup != None:
			return Operand(labelLookup, OperandType.LABEL, True)
		# Next check if it's an immediate
		elif address[0] == '#':
			return Operand(int(address[1:]), OperandType.IMMEDIATE, True)
	 	# Nect check if it's a register
		elif address[0] != 'R':
			return Operand(int(address[1:]), OperandType.REGISTER, True)
		# Dunno...quit
		else:
			raise Exception("Invalid syntax in instruction: " + address)

	def getOperand(self, operandIndex):
   		if len(self.operands) > operandIndex: 
   			return self.operands[operandIndex]

class Operand():

	def __init__(self, value, operandType, memoryLookup):
		self.value = value
		self.type = operandType
		self.memoryLookup = memoryLookup