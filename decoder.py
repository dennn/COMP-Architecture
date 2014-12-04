from pipelineStage import PipelineStage

class DecodeUnit(PipelineStage):

	def __init__(self, simulator):
		super(DecodeUnit, self).__init__(simulator)

	def clockTick(self):
		self.currentInstruction = self.simulator.fetchUnit.getNextInstruction()
		if self.currentInstruction is not None:
			self.decode()

	def decode(self):
		if opcode == 'LDR':
			self.decodeLDR()
		elif opcode == 'STR':
			self.STR()
		elif opcode == 'ADD' or opcode == 'SUB:
			self.decodeTypeOne()
		elif opcode == 'B' 
		  or opcode == 'BNE'
		  or opcode == 'BEQ'
		  or opcode == 'BLT'
		  or opcode == 'BGT':
			self.decodeTypeTwo()
		elif opcode == 'HALT':
			pass
		else:
			raise Exception("Couldn't find opcode " + opcode)
		self.nextInstruction = self.currentInstruction

# Decodes instructions of format ADD, SUB
	def decodeTypeOne(self):
		instruction = self.currentInstruction

		# Get all the operands
		destination = instruction.operands[0]
		operand1 = instruction.operands[1]
		if len(instruction.operands) > 2:
			operand2 = instruction.operands[2]
		else:
			operand2 = None

		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for ADD operation

		if operand2 is not None:
			if operand2.type == OperandType.REGISTER:
				val2 = self.registers[operand2.value]
			elif operand2.type == OperandType.IMMEDIATE:
				val2 = operand2.value
			else:
				raise Exception("Couldn't load operand 2 for ADD operation")

		# Put the decoded operands into the instruction
		self.currentInstruction.decodedOperands[0] = destination
		self.currentInstruction.decodedOperands[1] = val1
		if operand2 is not None:
			self.currentInstruction.decodedOperands[2] = val2

# Decodes instructions of format B, BEQ, BNE, BLT, BGT
	def decodeTypeTwo(self):
		instruction = self.currentInstruction

		# Get all the operands
		label = instruction.operands[0]

		if label.type != OperandType.LABEL:
			raise Exception("Invalid label for " + instruction.opcode + " operation")

		if len(instruction.operands > 1):
			# Get all the operands
			operand0 = instruction.operands[1]
			operand1 = instruction.operands[2]

			# Load operand 0 value
			if operand0.type == OperandType.REGISTER:
				val1 = self.registers[operand0.value]
			elif operand0.type == OperandType.IMMEDIATE:
				val1 = operand0.value
			else:
				raise Exception("Couldn't load operand 0 for " + instruction.opcode + " operation")

			# Load operand 1 value
			if operand1.type == OperandType.REGISTER:
				val2 = self.registers[operand1.value]
			elif operand1.type == OperandType.IMMEDIATE:
				val2 = operand1.value
			else:
				raise Exception("Couldn't load operand 1 for " + instruction.opcode + " operation")

		# Put the decoded operands into the instruction
		self.currentInstruction.decodedOperands[0] = destination
		if val1 is not None:
			val1 = int(val1)
			self.currentInstruction.decodedOperands[1] = val1
		if val2 is not None:
			val2 = int(val2)
			self.currentInstruction.decodedOperands[2] = val2

# Decode instruction of format LDR
	def decodeLDR(self):
		# Get all the operands
		destination = instruction.operands[0]
		operand1 = instruction.operands[1]
		if len(instruction.operands) > 2:
			operand2 = instruction.operands[2]
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
					offset = self.registers[operand2.value]
				else:
					offset = operand2.value
			address += offset

		# Put the decoded operands into the instruction
		self.currentInstruction.decodedOperands[0] = destination
		self.currentInstruction.decodedOperands[1] = operand1
		if address is not None:
			self.currentInstruction.decodedOperands[2] = address

# Decode instruction of format STR
	def decodeSTR(self):
		# Get all the operands
		valueOperand = instruction.operands[0]
		# Get the value to be stored out of the register
		if valueOperand.type == OperandType.REGISTER:
			value = self.registers[valueOperand.value]
		else:
			value = valueOperand.value

		destination = instruction.operands[1]
		if len(instruction.operands) > 2:
			offsetOperand = instruction.operands[2]
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
					offset = self.registers[offsetOperand.value]
				else:
					offset = offset.value
			address += offset

		# Put the decoded operands into the instruction
		self.currentInstruction.decodedOperands[0] = value
		if address is not None:
			self.currentInstruction.decodedOperands[1] = address
