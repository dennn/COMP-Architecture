import sys
from memory import *
from config import *
from assembler import *
from instruction import *

class Processor:

	def __init__(self, args):
		self.arguments = args

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

		print "Finished executing. Cycles: " + str(self.cycles)
		self.memory.printMemory()

	def execute(self, instruction):
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
		if operand2 is not None:
			self.registers[destination.value] = val1 + val2
		else:
			self.registers[destination.value] += val1

	def SUB(self, instruction):
		if operand2 is not None:
			self.registers[destination.value] = val1 - val2
		else:
			self.registers[destination.value] -= val1

	# Branches
	def B(self, instruction):
		self.pc = label.value.memoryLocation

	def BNE(self, instruction):		
		# Do the comparison
		if int(val0) != int(val1):
				self.pc = label.value.memoryLocation
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