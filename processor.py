import sys
from memory import *
from config import *
from Instructions import *
from Instructions.instruction import InstructionType
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
			if self.simulator.args.step:
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
				self.printMemory()
				raw_input("\n Press enter to continue..")	

		print "Finished executing. Cycles: " + str(self.clockCycles)
		if self.simulator.args.step == False:
			self.printRegisters(True)
			self.printMemory(True)		

	def checkForEmptyQueues(self):
		if len(self.instructionsToExecute) == 0 and \
		   len(self.instructionsToDecode) == 0 and \
		   len(self.instructionsToWriteback) == 0:
			self.continueRunning = False;

		return True

	def printRegisters(self, forced=False):
		if self.arguments.step or forced:
			for idx, register in enumerate(self.registers):
				print "R" + str(idx) + "=" + str(register) + ", "
			print "\n"

	def printMemory(self, forced=False):
		if self.arguments.step or forced:
			self.memory.printMemory()

###################################################
## FETCH STAGE
###################################################

	def fetch(self):
		# If we've reached the end of the program, there's nothing else to fetch
		if self.pc >= len(self.program.instructions):
			if self.simulator.args.step:
				print "FETCH STAGE: All instructions have been fetched"
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

		decodedInstruction = instructionToDecode.decode(self)
		opcode = decodedInstruction.opcode

		if self.dependenciesExist(decodedInstruction) == False:
			# If we have a branch, let's try and take it as early as possible 
			if decodedInstruction.instructionType == InstructionType.BRANCH:	
				if decodedInstruction.willTakeBranch(self) == True:
					if self.simulator.args.step:
						print "DECODE STAGE: Branching\n"

					# Flush all the buffers
					del self.instructionsToDecode[:]
				#	del self.instructionsToExecute[:]
				#	del self.instructionsToWriteback[:]
			else:
				self.instructionsToExecute.append(decodedInstruction)
		else:
			if self.simulator.args.step:
				print "**** DEPENDENCY: Dependencies exist, stalling *****\n" 

	def dependenciesExist(self, instruction):

		sourceRegister1 = instruction.getOperand(1)
		sourceRegister2 = instruction.getOperand(2)

		if instruction.opcode == 'STR':
			sourceRegister1 = instruction.getOperand(0)

		for innerInstruction in self.instructionsToExecute:
			if innerInstruction.destinationRegister == None:
				continue

			if (sourceRegister1 != None and sourceRegister1.value == innerInstruction.destinationRegister) or (sourceRegister2 != None and sourceRegister2.value == innerInstruction.destinationRegister):
				self.instructionsToDecode.insert(0, instruction)
				return True

		for innerInstruction in self.instructionsToWriteback:
			if innerInstruction.destinationRegister == None:
				continue

			if (sourceRegister1 != None and sourceRegister1.value == innerInstruction.destinationRegister) or (sourceRegister2 != None and sourceRegister2.value == innerInstruction.destinationRegister):
				self.instructionsToDecode.insert(0, instruction)
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

		instruction.execute(self)

		self.instructionsToWriteback.append(instruction)		

###################################################
## WRITEBACK STAGE
###################################################

	def writeBack(self):
		if len(self.instructionsToWriteback) == 0:
			if self.simulator.args.step:
				print "WRITEBACK STAGE: No Instructions in Queue\n"
			return

		instructionToWriteback = self.instructionsToWriteback.pop(0)
		if self.simulator.args.step:
			print "WRITEBACK STAGE: Writing back instruction " + str(instructionToWriteback) + "\n"

		instructionToWriteback.writeback(self)