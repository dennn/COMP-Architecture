import sys

# Define the architecture size, this affects the memory and number of registers
ARCH = 8

class Processor:

	def __init__(self):
		self.reset()

	def reset(self):
		self.pc = 0
		self.memory = Memory()
		self.registers = [0] * ARCH
		self.labels = {}
		self.instructions = []

	def run(self, instructionFile):
		instructionCount = 0
		for string in instructionFile:
			instructionList = string.split()
			# We've got an empty line
			if len(instructionList) == 0:
				continue
			# Check if we have a label or an opcode
			operation = instructionList[0]
			if operation[-1:] == ':':
				self.labels[operation[:-1]] = instructionCount
			else:
				self.instructions.append(instructionList)
				instructionCount += 1

		self.fetch()

	def fetch(self):
		while self.pc < len(self.instructions):
			instruction = self.instructions[self.pc]
			operation = instruction[0]
			self.execute(operation, instruction[1:])

	def execute(self, opcode, operands):
		self.pc += 1
		if opcode == 'LDR':
			self.LDR(operands[0], operands[1])
		elif opcode == 'STR':
			self.STR(operands[0], operands[1])
		elif opcode == 'ADD':
			self.ADD(operands[0], operands[1])
		elif opcode == 'SUB':
			self.SUB(operands[0], operands[1])
		elif opcode == 'B':
			self.B(operands[0])
		elif opcode == 'HALT':
			self.HALT()
		elif opcode == 'BNE':
			self.BNE(operands[0], operands[1])
		elif opcode == 'CMP':
			self.CMP(operands[0], operands[1], operands[2])
		else:
			print "couldn't find opcode " + opcode

	def printRegisters(self):
		for idx, register in enumerate(self.registers):
			print "R" + str(idx) + "=" + str(register) + ", "
		print "\n"

	def parseRegister(self, reg):
		return int(reg[1:].replace(',', ''))

	def parseAddress(self, address):
		if address[1] == '#':
			return int(address[2:-2])
		else:
			reg = self.parseRegister(address[1:-2])
			return self.registers[reg]

	# Instructions
	def LDR(self, r0, r1):
		r0 = self.parseRegister(r0)
		if r1[0] == '#':
			constant = int(r1[1:])
			self.registers[r0] = constant
		elif r1[0] == '[' and r1[:-1] == ']':
			address = parseAddress(r1)
			self.registers[r0] = self.memory.load(address)
		else:
			r1 = self.parseRegister(r1)
			self.registers[r0] = self.registers[r1]

	def STR(self, addr, r1):
		address = self.parseAddress(addr)
		if r1[0] == '#':
			constant = int(r1[1:])
			self.memory.store(address, constant)
		else:
			r1 = self.parseRegister(r1)
			self.memory.store(address, self.registers[r1])
		self.memory.printMemory()

	def ADD(self, r0, r1):
		r0 = self.parseRegister(r0)
		if r1[0] == '#':
			constant = int(r1[1:])
			self.registers[r0] += constant
		else:
			r1 = self.parseRegister(r1)
			self.registers[r0] += self.registers[r1]

	def SUB(self, r0, r1):
		r0 = self.parseRegister(r0)
		if r1[0] == '#':
			constant = int(r1[1:])
			self.registers[r0] -= constant
		else:
			r1 = self.parseRegister(r1)
			self.registers[r0] -= self.registers[r1]
		self.printRegisters()

	def B(self, label):
		labelPC = self.labels[label]
		self.pc = labelPC

	def BNE(self, r0, label):
		r0 = self.parseRegister(r0)
		if self.registers[r0] != 0:
			labelPC = self.labels[label]
			self.pc = labelPC

	def CMP(self, result, r1, r2):
		if r1[0] == '#':
			val1 = int(r1[1:])
		else:
			r1 = self.parseRegister(r1)
			val1 = self.registers[r1]

		if r2[0] == '#':
			val2 = int(r2[1:])
		else:
			r2 = self.parseRegister(r2)
			val2 = self.registers[r2]

		result = self.parseRegister(result)
		if val1 > val2:
			self.registers[result] = 1
		elif val1 == val2:
			self.registers[result] = 0
		elif val1 < val2:
			self.registers[result] = -1

	def HALT(self):
		print "Halting"

class Memory:

	def __init__(self):
		self.reset()

	def load(self, address):
		if address < 0 or address >= len(self.data):
			raise Exception("Access violation at " + address)

		return self.data[address]

	def store(self, address, value):
		if address < 0 or address >= len(self.data):
			raise Exception("Access violation at " + address)

		self.data[address] = value

	def printMemory(self):
		for i in self.data:
			sys.stdout.write(str(i) + " ")
		print

	def reset(self):
		self.data = [0] * pow(2, ARCH)


def main():
	cpu = Processor()
	programFile = open("Programs/add.asm", "r")
	cpu.run(programFile)
	programFile.close()

if __name__ == '__main__':
	main()