class OperandType():
	REGISTER, IMMEDIATE, LABEL = range(3)

class InstructionType():
	ALU, BRANCH, MEMORY, OTHER = range(4)

class Operand():

	def __init__(self, value, operandType, memoryLookup):
		self.value = value
		self.type = operandType
		self.memoryLookup = memoryLookup

class Instruction():

	def __init__(self, line, assembler):
		self.rawInstruction = line
		self.opcode = None
		self.operands = []
		self.assembler = assembler
		self.parseInstruction()

	def __str__(self):
		return ' '.join(self.rawInstruction)

	# Methods for the subclasses to implement
	def execute(self, processor):
		pass 

	def writeback(self, processor):
		pass

	# Do the actual decoding
	def decode(self, processor):
		if self.opcode == 'ADD' or self.opcode == 'SUB' or self.opcode == 'MUL' or self.opcode == 'DIV':
			return self.decodeTypeOne(processor)
		elif self.opcode == 'B' or self.opcode == 'BEQ' or self.opcode == 'BNE' or self.opcode == 'BGT' or self.opcode == 'BLT':
			return self.decodeTypeTwo(processor)
		elif self.opcode == 'LDR':
			return self.decodeLDR(processor)
		elif self.opcode == 'STR':
			return self.decodedSTR(processor)
		elif self.opcode == 'HALT':
			return self.decodedHALT()
		else:
			raise Exception("Unknown opcode " + self.opcode)

	# Instruction parsing
	def parseInstruction(self):
		self.opcode = self.rawInstruction[0]
		for operand in self.rawInstruction[1:]:
			self.operands.append(self.parseValue(operand))

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

   	# Decodes instructions of format ADD, SUB
	def decodeTypeOne(self, processor):

		# Check we have 3 operands
		if len(self.operands) != 3:
			raise Exception("Not enough operands for instruction " + str(self))

		# Get all the operands
		destination = self.operands[0]
		operand1 = self.operands[1]
		operand2 = self.operands[2]

		if operand1.type == OperandType.REGISTER:
			val1 = processor.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for instruction " + str(self))

		if operand2.type == OperandType.REGISTER:
			val2 = processor.registers[operand2.value]
		elif operand2.type == OperandType.IMMEDIATE:
			val2 = operand2.value
		else:
			raise Exception("Couldn't load operand 2 for instruction " + str(self))

		# Put the decoded operands into the instruction
		if self.opcode == 'ADD':
			from Instructions.ADD import ADD

			decodedInstruction = ADD(self)
			decodedInstruction.decodedOperands.extend([destination, val1, val2])
			decodedInstruction.destinationRegister = destination.value
		elif self.opcode == 'SUB':
			from Instructions.SUB import SUB

			decodedInstruction = SUB(self)
			decodedInstruction.decodedOperands.extend([destination, val1, val2])
			decodedInstruction.destinationRegister = destination.value
		elif self.opcode == 'MUL':
			from Instructions.MUL import MUL

			decodedInstruction = MUL(self)
			decodedInstruction.decodedOperands.extend([destination, val1, val2])
			decodedInstruction.destinationRegister = destination.value
		elif self.opcode == 'DIV':
			from Instructions.DIV import DIV

			decodedInstruction = DIV(self)
			decodedInstruction.decodedOperands.extend([destination, val1, val2])
			decodedInstruction.destinationRegister = destination.value
		else:
			raise Exception("Decoding unknown opcode")

		return decodedInstruction

	# Decodes instructions of format B, BEQ, BNE, BLT, BGT
	def decodeTypeTwo(self, processor):

		# Get all the operands
		label = self.operands[0]

		if label.type != OperandType.LABEL:
			raise Exception("Invalid label for " + self.opcode + " operation")

		if len(self.operands) > 1:
			# Get all the operands
			operand0 = self.operands[1]
			operand1 = self.operands[2]

			# Load operand 0 value
			if operand0.type == OperandType.REGISTER:
				val1 = processor.registers[operand0.value]
			elif operand0.type == OperandType.IMMEDIATE:
				val1 = operand0.value
			else:
				raise Exception("Couldn't load operand 0 for " + self.opcode + " operation")

			# Load operand 1 value
			if operand1.type == OperandType.REGISTER:
				val2 = processor.registers[operand1.value]
			elif operand1.type == OperandType.IMMEDIATE:
				val2 = operand1.value
			else:
				raise Exception("Couldn't load operand 1 for " + self.opcode + " operation")

		# Put the decoded operands into the instruction
		if self.opcode == 'B':
			from Instructions.B import B

			decodedInstruction = B(self)
			decodedInstruction.decodedOperands.append(label)
		elif self.opcode == 'BEQ':
			from Instructions.BEQ import BEQ

			decodedInstruction = BEQ(self)
			decodedInstruction.decodedOperands.append(label)
			if val1 is not None:
				val1 = int(val1)
				decodedInstruction.decodedOperands.append(val1)
			if val2 is not None:
				val2 = int(val2)
				decodedInstruction.decodedOperands.append(val2)
		elif self.opcode == 'BNE':
			from Instructions.BNE import BNE

			decodedInstruction = BNE(self)
			decodedInstruction.decodedOperands.append(label)
			if val1 is not None:
				val1 = int(val1)
				decodedInstruction.decodedOperands.append(val1)
			if val2 is not None:
				val2 = int(val2)
				decodedInstruction.decodedOperands.append(val2)
		elif self.opcode == 'BGT':
			from Instructions.BGT import BGT

			decodedInstruction = BGT(self)
			decodedInstruction.decodedOperands.append(label)
			if val1 is not None:
				val1 = int(val1)
				decodedInstruction.decodedOperands.append(val1)
			if val2 is not None:
				val2 = int(val2)
				decodedInstruction.decodedOperands.append(val2)
		elif self.opcode == 'BLT':
			from Instructions.BLT import BLT

			decodedInstruction = BLT(self)
			decodedInstruction.decodedOperands.append(label)
			if val1 is not None:
				val1 = int(val1)
				decodedInstruction.decodedOperands.append(val1)
			if val2 is not None:
				val2 = int(val2)
				decodedInstruction.decodedOperands.append(val2)
		else:
			raise Exception("Decoding unkown opcode")

		return decodedInstruction

	# Decode instruction of format LDR
	def decodeLDR(self, processor):

		address = None
		# Get all the operands
		destination = self.operands[0]
		operand1 = self.operands[1]
		if len(self.operands) > 2:
			operand2 = self.operands[2]
		else:
			operand2 = None

		# Is it a memory type of operation
		if operand1.memoryLookup == True:
			offset = 0
			if operand1.type == OperandType.LABEL:
				address = operand1.value.memoryLocation
			else:
				address = operand1.value
			if operand2 is not None:
				if operand2.type == OperandType.REGISTER:
					offset = processor.registers[operand2.value]
				else:
					offset = operand2.value
			address += offset

		from Instructions.LDR import LDR

		decodedInstruction = LDR(self)
		decodedInstruction.destinationRegister = destination.value
		decodedInstruction.decodedOperands.append(destination)
		if address:
			decodedInstruction.decodedOperands.append(address)
		else:
			decodedInstruction.decodedOperands.append(operand1.value)

		return decodedInstruction

	# Decode instruction of format STR
	def decodedSTR(self, processor):

		valueOperand = self.operands[0]
		# Get the value to be stored out of the register
		if valueOperand.type == OperandType.REGISTER:
			value = processor.registers[valueOperand.value]
		else:
			value = valueOperand.value

		destination = self.operands[1]
		if len(self.operands) > 2:
			offsetOperand = self.operands[2]
		else:
			offsetOperand = None

		# Is it a memory type of operation
		if destination.memoryLookup == True:
			offset = 0
			if destination.type == OperandType.LABEL:
				address = destination.value.memoryLocation
			else:
				address = destination.value
			if offsetOperand is not None:
				if offsetOperand.type == OperandType.REGISTER:
					offset = processor.registers[offsetOperand.value]
				else:
					offset = offset.value
			address += offset

		from Instructions.STR import STR

		decodedInstruction = STR(self)
		decodedInstruction.decodedOperands.append(value)
		if address is not None:
			decodedInstruction.decodedOperands.append(address)

		return decodedInstruction

	# Decoded instruction of format HALT
	def decodedHALT(self):
		from Instructions.HALT import HALT

		decodedInstruction = HALT(self)
		return decodedInstruction
