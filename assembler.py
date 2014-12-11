from sets import Set
from instruction import Instruction

class Assembler():
	
	def __init__(self, memory, args):
		self.instructions = []
		self.labels = {}
		self.memory = memory
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
		tempInstructions = []

		# Now get all the instructions, labels and data values
		for string in instructionFile:
			string = self.cleanString(string)
			string = self.removeComments(string)
			instructionList = string.split()
			# We've got an empty line
			if len(instructionList) == 0:
				continue
			# Check if we have a label or an opcode
			operation = instructionList[0]
			if operation[-1:] == ':':
				if len(instructionList) > 1:
					raise Exception("A label can't have an instruction on the same line")
				label = Label(instructionCount, operation[:-1])
				self.labels[label.labelString] = label
				continue
			elif operation == '.data':
				self.memory.store(instructionCount, instructionList[1])
			else:
				tempInstructions.append(instructionList)
			instructionCount += 1

		# Now convert the instructions to actual instructions
		for instruction in tempInstructions:
			newInstruction = Instruction(instruction, self)
			self.instructions.append(newInstruction)

	def removeComments(self, string):
		if string.startswith("#"):
			return ""
		else:
			return string

	def cleanString(self, string):
		string = string.strip()
		string = string.replace(',', '')

		return string

	def labelLookup(self, label):
		if label in self.labels:
			return self.labels[label]
		else:
			return None

class Label():

	def __init__(self, memoryLocation, label):
		self.memoryLocation = memoryLocation
		self.labelString = label
