import sys
from memory import *
from config import *
from assembler import *

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
			operation = instruction[0]
			if self.arguments.step:
				print "----------------------------"
				self.printRegisters()
				print "Current instruction: " + ' '.join(instruction)
			self.execute(operation, instruction[1:])
			self.printRegisters()
			self.cycles += 1

		print "Finished executing. Cycles: " + str(self.cycles)
		self.memory.printMemory()

	def execute(self, opcode, operands):
		operands = [operand.strip(",") for operand in operands]

		self.pc += 1
		if opcode == 'LDR':
			if len(operands) == 2:
				self.LDR(operands[0], operands[1], None)
			else:
				self.LDR(operands[0], operands[1], operands[2])
		elif opcode == 'STR':
			if len(operands) == 2:
				self.STR(operands[0], operands[1], None)
			else:
				self.STR(operands[0], operands[1], operands[2])
		elif opcode == 'ADD':
			if len(operands) == 2:
				self.ADD(operands[0], operands[1], None)
			else:
				self.ADD(operands[0], operands[1], operands[2])
		elif opcode == 'SUB':
			self.SUB(operands[0], operands[1])
		elif opcode == 'B':
			self.B(operands[0])
		elif opcode == 'HALT':
			self.HALT()
		elif opcode == 'BNE':
			self.BNE(operands[0], operands[1], operands[2])
		elif opcode == 'BEQ':
			self.BEQ(operands[0], operands[1], operands[2])
		elif opcode == 'BLT':
			self.BLT(operands[0], operands[1], operands[2])
		elif opcode == 'BGT':
			self.BGT(operands[0], operands[1], operands[2])
		else:
			raise Exception("Couldn't find opcode " + opcode)

	def printRegisters(self):
		if self.arguments.step:
			for idx, register in enumerate(self.registers):
				print "R" + str(idx) + "=" + str(register) + ", "
			print "\n"

	def parseRegister(self, reg):
		return int(reg[1:])

	def parseAddress(self, address):
		address = address.replace(',', '')
		address = address.replace(']', '')
		address = address.replace('[', '')
		if address in self.program.labels:
			labelLookup = self.program.labels[address]
			return labelLookup.memoryLocation
		elif address[0] == '#':
			return int(address[1:])
		else:
			reg = self.parseRegister(address[1:-2])
			return self.registers[reg]

	# Memory Access
	def LDR(self, r0, r1, r2):
		r0 = self.parseRegister(r0)
		r1 = r1.replace(',', '')
		if r1[0] == '#':
			constant = int(r1[1:])
			self.registers[r0] = constant
		elif r1[0] == '[' and r1[-1:] == ']':
			address = self.parseAddress(r1)
			if r2 is not None:
				if (r2[0] == '#'):
					offset = int(r2[1:])
				else:
					reg = self.parseRegister(r2)
					offset = self.registers[reg]
				address += offset
				if self.arguments.step:
					self.memory.printMemory()
			self.registers[r0] = self.memory.load(address)
		else:
			r1 = self.parseRegister(r1)
			self.registers[r0] = self.registers[r1]

	def STR(self, r1, addr, r2):
		address = self.parseAddress(addr)
		offset = 0
		if r2 is not None:
			if (r2[0] == '#'):
				offset = int(r2[1:])
			else:
				reg = self.parseRegister(r2)
				offset = self.registers[reg]
		if r1[0] == '#':
			constant = int(r1[1:])
			self.memory.store(address + offset, constant)
		else:
			r1 = self.parseRegister(r1)
			self.memory.store(address + offset, self.registers[r1])
		if self.arguments.step:
			self.memory.printMemory()

	# ALU
	def ADD(self, destinationRegister, r1, r2):
		destinationRegister = self.parseRegister(destinationRegister)
		if r2 is not None:		
			r1 = self.parseRegister(r1)
			if r2[0] == '#':
				constant = int(r2[1:])
				self.registers[destinationRegister] = self.registers[r1] + constant
			else:
				r2 = self.parseRegister(r2)
				self.registers[destinationRegister] = self.registers[r1] + self.registers[r2]
		else:
			if r1[0] == '#':
				constant = int(r1[1:])
				self.registers[destinationRegister] += constant
			else:
				r1 = self.parseRegister(r1)
				self.registers[destinationRegister] += self.registers[r1]

	def SUB(self, r0, r1):
		r0 = self.parseRegister(r0)
		if r1[0] == '#':
			constant = int(r1[1:])
			self.registers[r0] -= constant
		else:
			r1 = self.parseRegister(r1)
			self.registers[r0] -= self.registers[r1]

	# Branches
	def B(self, label):
		labelPC = self.program.labels[label]
		self.pc = labelPC.memoryLocation

	def BNE(self, val1, val2, label):
		if val1[0] == '#':
			val1 = int(val1[1:])
		else:
			r1 = self.parseRegister(val1)
			val1 = int(self.registers[r1])

		if val2[0] == '#':
			val2 = int(val2[1:])
		else:
			r2 = self.parseRegister(val2)
			val2 = int(self.registers[r2])

		if val1 != val2:
			labelPC = self.program.labels[label]
			self.pc = labelPC.memoryLocation		

	def BEQ(self, val1, val2, label):
		if val1[0] == '#':
			val1 = int(val1[1:])
		else:
			r1 = self.parseRegister(val1)
			val1 = int(self.registers[r1])

		if val2[0] == '#':
			val2 = int(val2[1:])
		else:
			r2 = self.parseRegister(val2)
			val2 = int(self.registers[r2])

		if val1 == val2:
			labelPC = self.program.labels[label]
			self.pc = labelPC.memoryLocation		


	def BLT(self, val1, val2, label):
		if val1[0] == '#':
			val1 = int(val1[1:])
		else:
			r1 = self.parseRegister(val1)
			val1 = int(self.registers[r1])

		if val2[0] == '#':
			val2 = int(val2[1:])
		else:
			r2 = self.parseRegister(val2)
			val2 = int(self.registers[r2])

		if val1 < val2:
			labelPC = self.program.labels[label]
			self.pc = labelPC.memoryLocation	

	def BGT(self, val1, val2, label):
		if val1[0] == '#':
			val1 = int(val1[1:])
		else:
			r1 = self.parseRegister(val1)
			val1 = int(self.registers[r1])

		if val2[0] == '#':
			val2 = int(val2[1:])
		else:
			r2 = self.parseRegister(val2)
			val2 = int(self.registers[r2])

		if val1 > val2:
			labelPC = self.program.labels[label]
			self.pc = labelPC.memoryLocation	

	# Other
	def HALT(self):
		print "Halting"