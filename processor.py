import sys
from memory import *
from config import *
from assembler import *
from instruction import *

class Processor:

	def __init__(self, args):
		self.arguments = args
		self.reset()

	def reset(self):
		self.pc = 0
		self.memory = Memory()
		self.registers = [0] * ARCH
		self.cycles = 0

	def run(self, assembledProgram):
		self.program = assembledProgram
		self.fetch()

	def fetch(self):
		while self.pc < len(self.program.instructions):
			instruction = self.program.instructions[self.pc]
			if self.arguments.step:
				print "----------------------------"
				self.printRegisters()
				print "Current instruction: "
				print instruction
				print
			self.execute(instruction)
			self.printRegisters()
			self.cycles += 1

		print "Finished executing. Cycles: " + str(self.cycles)
		self.memory.printMemory()

	def execute(self, instruction):
		self.pc += 1
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
			raise Exception("Couldn't load operand 1 for ADD operation")

		if operand2 is not None:
			if operand2.type == OperandType.REGISTER:
				val2 = self.registers[operand2.value]
			elif operand2.type == OperandType.IMMEDIATE:
				val2 = operand2.value
			else:
				raise Exception("Couldn't load operand 2 for ADD operation")
			self.registers[destination.value] = val1 + val2
		else:
			self.registers[destination.value] += val1

	def SUB(self, instruction):
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
			raise Exception("Couldn't load operand 1 for SUB operation")

		if operand2 is not None:
			if operand2.type == OperandType.REGISTER:
				val2 = self.registers[operand2.value]
			elif operand2.type == OperandType.IMMEDIATE:
				val2 = operand2.value
			else:
				raise Exception("Couldn't load operand 2 for SUB operation")
			self.registers[destination.value] = val1 - val2
		else:
			self.registers[destination.value] -= val1

	# Branches
	def B(self, instruction):
		# Get all the operands
		label = instruction.operands[0]

		if label.type != OperandType.LABEL:
			raise Exception("Invalid label for B operation")
		else:
			self.pc = label.value.memoryLocation

	def BNE(self, instruction):
		# Get all the operands
		operand0 = instruction.operands[0]
		operand1 = instruction.operands[1]
		label = instruction.operands[2]

		# Load operand 0 value
		if operand0.type == OperandType.REGISTER:
			val0 = self.registers[operand0.value]
		elif operand0.type == OperandType.IMMEDIATE:
			val0 = operand0.value
		else:
			raise Exception("Couldn't load operand 0 for BEQ operation")

		# Load operand 1 value
		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for BEQ operation")
		
		# Do the comparison
		if int(val0) != int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BNE operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"		

	def BEQ(self, instruction):
		# Get all the operands
		operand0 = instruction.operands[0]
		operand1 = instruction.operands[1]
		label = instruction.operands[2]

		# Load operand 0 value
		if operand0.type == OperandType.REGISTER:
			val0 = self.registers[operand0.value]
		elif operand0.type == OperandType.IMMEDIATE:
			val0 = operand0.value
		else:
			raise Exception("Couldn't load operand 0 for BEQ operation")

		# Load operand 1 value
		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for BEQ operation")
		
		# Do the comparison
		if int(val0) == int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BEQ operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"	


	def BLT(self, instruction):
		# Get all the operands
		operand0 = instruction.operands[0]
		operand1 = instruction.operands[1]
		label = instruction.operands[2]

		# Load operand 0 value
		if operand0.type == OperandType.REGISTER:
			val0 = self.registers[operand0.value]
		elif operand0.type == OperandType.IMMEDIATE:
			val0 = operand0.value
		else:
			raise Exception("Couldn't load operand 0 for BLT operation")

		# Load operand 1 value
		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for BLT operation")
		
		# Do the comparison
		if int(val0) < int(val1):
			if label.type != OperandType.LABEL:
				raise Exception("Invalid label for BLT operation")
			else:
				self.pc = label.value.memoryLocation
				if self.arguments.step:
					print "Branching"

	def BGT(self, instruction):
		# Get all the operands
		operand0 = instruction.operands[0]
		operand1 = instruction.operands[1]
		label = instruction.operands[2]

		# Load operand 0 value
		if operand0.type == OperandType.REGISTER:
			val0 = self.registers[operand0.value]
		elif operand0.type == OperandType.IMMEDIATE:
			val0 = operand0.value
		else:
			raise Exception("Couldn't load operand 0 for BGT operation")

		# Load operand 1 value
		if operand1.type == OperandType.REGISTER:
			val1 = self.registers[operand1.value]
		elif operand1.type == OperandType.IMMEDIATE:
			val1 = operand1.value
		else:
			raise Exception("Couldn't load operand 1 for BGT operation")
		
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