import sys
from memory import *
from config import *
from assembler import *
from instruction import *
import Queue

class Processor:

	def __init__(self, simulator, memory, arguments):
		self.arguments = arguments
		self.registers = [0] * ARCH
		self.pc = 0
		self.clockCycles = 0
		self.memory = memory
		self.simulator = simulator
		self.instructionsToExecute = []
		self.instructionsToDecode = []
		self.instructionsToWriteback = []
		self.continueRunning = True

	def run(self, assembledProgram):
		self.program = assembledProgram
		while self.continueRunning == True:
			print "---------------------"
			self.printRegisters()
			self.writeBack()
			self.execute()
			self.decode()
			self.fetch()

			self.clockCycles += 1

			self.checkForEmptyQueues()		

			if self.simulator.args.step:
				self.printRegisters()
				raw_input("Press enter to continue..")	

		print "Finished executing. Cycles: " + str(self.clockCycles)
		if self.simulator.args.step:
			self.memory.printMemory()			

	def checkForEmptyQueues(self):
		if len(self.instructionsToExecute) == 0 and \
		   len(self.instructionsToDecode) == 0 and \
		   len(self.instructionsToWriteback) == 0:
			self.continueRunning = False;

		return True

###################################################
## FETCH STAGE
###################################################

	def fetch(self):
		# If we've reached the end of the program, there's nothing else to fetch
		if self.pc >= len(self.program.instructions):
			return

		instruction = self.program.instructions[self.pc]
		if self.simulator.args.step:
			print "FETCH STAGE: " + str(instruction) + "\n"
		self.instructionsToDecode.append(instruction)
		self.pc += 1

###################################################
## DECODE STAGE
###################################################

	def decode(self):
		# If there are no instructions that can be decoded, just return
		if len(self.instructionsToDecode) == 0:
			if self.simulator.args.step:
				print "DECODE STAGE: No Instructions in Queue\n"
			return

		instructionToDecode = self.instructionsToDecode.pop(0)
		if self.simulator.args.step:
			print "DECODE STAGE: Decoding instruction " + str(instructionToDecode) + "\n"

		opcode = instructionToDecode.opcode

		if opcode == 'LDR':
			instructionToDecode = self.decodeLDR(instructionToDecode)
		elif opcode == 'STR':
			instructionToDecode = self.decodeSTR(instructionToDecode)
		elif opcode == 'ADD' or opcode == 'SUB':
			instructionToDecode = self.decodeTypeOne(instructionToDecode)
		elif opcode == 'B' or opcode == 'BNE' or opcode == 'BEQ' or opcode == 'BLT' or opcode == 'BGT':
			instructionToDecode = self.decodeTypeTwo(instructionToDecode)
		elif opcode == 'HALT':
			pass
		else:
			raise Exception("Couldn't find opcode " + opcode)

		if self.dependenciesExist(instructionToDecode) == False:
			self.instructionsToExecute.append(instructionToDecode)
		else:
			if self.simulator.args.step:
				print "****DEPENDENCY: Dependencies exist, stalling*****" 

	# Decodes instructions of format ADD, SUB
	def decodeTypeOne(self, instruction):

		# Check we have 3 operands
		if len(instruction.operands) != 3:
			raise Exception("Not enough operands for instruction " + str(instruction))

		# Get all the operands
		destination = instruction.operands[0]
		operand1 = instruction.operands[1]
		operand2 = instruction.operands[2]

		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for instruction " + str(instruction))

		if operand2.type == OperandType.REGISTER:
			val2 = self.registers[operand2.value]
		elif operand2.type == OperandType.IMMEDIATE:
			val2 = operand2.value
		else:
			raise Exception("Couldn't load operand 2 for instruction " + str(instruction))

		# Put the decoded operands into the instruction
		instruction.decodedOperands = [None] * len(instruction.operands)
		instruction.decodedOperands[0] = destination
		instruction.decodedOperands[1] = val1
		instruction.decodedOperands[2] = val2
		instruction.destinationRegister = destination.value

		return instruction

# Decodes instructions of format B, BEQ, BNE, BLT, BGT
	def decodeTypeTwo(self, instruction):

		# Get all the operands
		label = instruction.operands[0]

		if label.type != OperandType.LABEL:
			raise Exception("Invalid label for " + instruction.opcode + " operation")

		if len(instruction.operands) > 1:
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
		instruction.decodedOperands = [None] * len(instruction.operands)
		instruction.decodedOperands[0] = label
		if val1 is not None:
			val1 = int(val1)
			instruction.decodedOperands[1] = val1
		if val2 is not None:
			val2 = int(val2)
			instruction.decodedOperands[2] = val2

		return instruction

# Decode instruction of format LDR
	def decodeLDR(self, instruction):

		address = None
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
		instruction.decodedOperands = [None] * len(instruction.operands)
		instruction.destinationRegister = destination
		instruction.decodedOperands[0] = destination
		instruction.decodedOperands[1] = operand1
		if address is not None:
			instruction.decodedOperands[2] = address

		return instruction

# Decode instruction of format STR
	def decodeSTR(self, instruction):
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
		instruction.decodedOperands = [None] * len(instruction.operands)
		instruction.decodedOperands[0] = value
		if address is not None:
			instruction.decodedOperands[1] = address

		return instruction

###################################################
## DEPENDENCY CHECKING
###################################################

	def dependenciesExist(self, instruction):

		sourceRegister1 = instruction.getOperand(1)
		sourceRegister2 = instruction.getOperand(2)

		print sourceRegister1.value
		if sourceRegister2 is not None:
			print sourceRegister2.value
		if instruction.destinationRegister is not None:
			print instruction.destinationRegister

		for innerInstruction in self.instructionsToExecute:

			if instruction.destinationRegister == None:
				continue

			if (sourceRegister1 != None and sourceRegister1 == innerInstruction.destinationRegister) or (sourceRegister2 != None and sourceRegister2 == innerInstruction.destinationRegister):
				raw_input('found dependency')
				self.instructionsToDecode.appendLeft(instruction)
				return True

		for innerInstruction in self.instructionsToWriteback:
			if instruction.destinationRegister == None:
				continue

			if (sourceRegister1 != None and sourceRegister1 == innerInstruction.destinationRegister) or (sourceRegister2 != None and sourceRegister2 == innerInstruction.destinationRegister):
				raw_input('found dependency')
				self.instructionsToDecode.appendLeft(instruction)
				return True

		return False

###################################################
## EXECUTE STAGE
###################################################

	def execute(self):
		if len(self.instructionsToExecute) == 0:
			if self.simulator.args.step:
				print "EXECUTE STAGE: No Instructions in Queue\n"
			return

		instruction = self.instructionsToExecute.pop(0)
		if self.simulator.args.step:
			print "EXECUTE STAGE: Executing instruction " + str(instruction) + "\n"

		opcode = instruction.opcode
		if opcode == 'LDR':
			self.LDR(instruction)
		elif opcode == 'STR':
			self.STR(instruction)
		elif opcode == 'ADD':
			self.ADD(instruction)
		elif opcode == 'SUB':
			self.SUB(instruction)
		elif opcode == 'B':
			self.B(instruction)
		elif opcode == 'BNE':
			self.BNE(instruction)
		elif opcode == 'BEQ':
			self.BEQ(instruction)
		elif opcode == 'BLT':
			self.BLT(instruction)
		elif opcode == 'BGT':
			self.BGT(instruction)
		elif opcode == 'HALT':
			self.HALT()
		else:
			raise Exception("Couldn't find opcode " + opcode)

		self.instructionsToWriteback.append(instruction)

	def printRegisters(self):
		if self.arguments.step:
			for idx, register in enumerate(self.registers):
				print "R" + str(idx) + "=" + str(register) + ", "
			print "\n"

	# Memory Access
	def LDR(self, instruction):
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
			self.registers[destination.value] = self.memory.load(address)
			if self.arguments.step:
				self.memory.printMemory()
		else:
			if operand1.type == OperandType.REGISTER:
				self.registers[destination.value] = self.registers[operand1.value]
			elif operand1.type == OperandType.IMMEDIATE:
				self.registers[destination.value] = operand1.value
			else:
				print "Fuck"

	def STR(self, instruction):
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
			self.memory.store(address, value)
			if self.arguments.step:
				self.memory.printMemory()

	# ALU
	def ADD(self, instruction):
		instruction.result = instruction.decodedOperands[1] + instruction.decodedOperands[2]

	def SUB(self, instruction):
		instruction.result = instruction.decodedOperands[1] - instruction.decodedOperands[2]

	# Branches
	def B(self, instruction):
		self.pc = label.value.memoryLocation

	def BNE(self, instruction):		
		instructionOperands = instruction.decodedOperands

		# Do the comparison
		if instructionOperands[1] != instructionOperands[2]:
				self.pc = instructionOperands[0].value.memoryLocation
				if self.arguments.step:
					print "Branching"		

	def BEQ(self, instruction):		
		# Do the comparison
		if int(val0) == int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BEQ operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"	


	def BLT(self, instruction):
		# Do the comparison
		if int(val0) < int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BLT operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"

	def BGT(self, instruction):
		# Do the comparison
		if int(val0) > int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BGT operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"

	# Other
	def HALT(self):
		print "Halting"

###################################################
## WRITEBACK STAGE
###################################################

	def writeBack(self):
		if len(self.instructionsToWriteback) == 0:
			if self.simulator.args.step:
				print "WRITEBACK STAGE: No Instructions in Queue\n"
			return

		instructionToWriteback = self.instructionsToWriteback.pop(0)

		if instructionToWriteback.result is not None:
			if self.simulator.args.step:
				print "WRITEBACK STAGE: Writing back instruction " + str(instructionToWriteback) + "\n"
			self.registers[instructionToWriteback.destinationRegister] = instructionToWriteback.result
		else:
			if self.simulator.args.step:
				print "WRITEBACK STAGE: Nothing to write back \n"