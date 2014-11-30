class Assembler():
	
	def __init__(self, cpu, args):
		self.instructions = []
		self.labels = {}
		self.cpu = cpu
		self.arguments = args
		self.readFile()

	def readFile(self):
		try:
			programFile = open(self.arguments.file, "r")
			self.parse(programFile)
		except IOError:
			raise Exception("Error Loading file")

		else:
			programFile.close()

	def parse(self, instructionFile):
		instructionCount = 0
		for string in instructionFile:
			string = string.strip()
			string = self.removeComments(string)
			instructionList = string.split()
			# We've got an empty line
			if len(instructionList) == 0:
				continue
			print instructionList
			# Check if we have a label or an opcode
			operation = instructionList[0]
			if operation[-1:] == ':':
				if len(instructionList) > 1:
					raise Exception("A label can't have an instruction on the same line")
				label = Label(instructionCount, operation[:-1])
				self.labels[label.labelString] = label
				continue
			elif operation == '.data':
				self.cpu.memory.store(instructionCount, instructionList[1])
			else:
				self.instructions.append(instructionList)
			instructionCount += 1

	def removeComments(self, string):
		if string.startswith("#"):
			return ""
		else:
			return string

class Label():

	def __init__(self, memoryLocation, label):
		self.memoryLocation = memoryLocation
		self.labelString = label
