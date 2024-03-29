# -*- coding: utf-8 -*-
from __future__ import division
import sys
import config
from memory import *
from branchpredictor import *
from Instructions import *
from Instructions.instruction import InstructionType
from Instructions.instruction import OperandType
from Units import *

class Processor:

	def __init__(self, memory, arguments):
		self.arguments = arguments
		# Memory and Registers
		self.memory = memory
		self.registers = [0] * config.REGISTERS

		self.initInternals()
		self.initUnits()
		self.initBuffers()

	def initInternals(self):
		# Processor Status
		self.pc = 0
		self.stalls = 0
		self.clockCycles = 0
		self.instructionsExecuted = 0
		self.continueRunning = True

	def initUnits(self):
		# Units
		self.ALUExecutionUnits = [ALUExecutionUnit(self, i) for i in range(config.NUMBER_EXECUTION_UNITS)]
		self.LSExecutionUnits = [LSExecutionUnit(self, i) for i in range(config.NUMBER_EXECUTION_UNITS)]
		self.branchPredictor = None
		if self.arguments.branchpredictor == True:
			self.branchPredictor = BranchPredictor(self)
		self.branchExecutionUnit = BranchExecutionUnit(self, self.branchPredictor)
		self.writebackUnit = WriteBackUnit(self)

	def initBuffers(self):
		# Buffers
		self.ALUInstructionsToExecute = [[] for i in range(config.NUMBER_EXECUTION_UNITS)]
		self.LSInstructionsToExecute = [[] for i in range(config.NUMBER_EXECUTION_UNITS)]
		self.instructionsToDecode = []
		self.instructionsToWriteback = []

	def run(self, assembledProgram):
		self.program = assembledProgram
		while self.continueRunning == True:
			if self.arguments.step:
				print "Cycle: " + str(self.clockCycles) + "\n"
				print "---------------------"

			self.printRegisters()
			self.writeBack()
			self.execute()

			for i in range(config.NUMBER_EXECUTION_UNITS):
				result = self.decode(i)
				if result is not True:
					break

			for i in range(config.NUMBER_EXECUTION_UNITS):
				result = self.fetch(i)
				if result is not True:
					break

			if self.checkForEmptyQueues() == True:
				self.continueRunning = False
			self.clockCycles += 1

			if self.arguments.step:
				self.printRegisters()
				self.printMemory()
				raw_input("\n Press enter to continue..")	

		self.printStats()
		if self.arguments.step == False:
			self.printRegisters(True)
			self.printMemory(True)		

	def checkForEmptyQueues(self, decodeIncluded=True):
		queuesEmpty = True

		# Check the execution units
		for i in range(config.NUMBER_EXECUTION_UNITS):
			# Check that the ALUs have no more instructions to execute, and aren't currently executing
			if len(self.ALUInstructionsToExecute[i]) != 0:
				queuesEmpty = False
			if self.ALUExecutionUnits[i].currentInstruction != None:
				queuesEmpty = False
			# Check that the LS units have no more instructions to execute, and aren't currently executing
			if len(self.LSInstructionsToExecute[i]) != 0:
			   	queuesEmpty = False
			if self.LSExecutionUnits[i].currentInstruction != None: 
				queuesEmpty = False

		# Check instructions to decode
		if decodeIncluded == True:
			if len(self.instructionsToDecode) != 0:
				queuesEmpty = False

		# Check instructions to writeback
		if len(self.instructionsToWriteback) != 0:
			queuesEmpty = False

		return queuesEmpty

	def clearAllBuffers(self):
		for i in range(config.NUMBER_EXECUTION_UNITS):
			del self.ALUInstructionsToExecute[i][:]
			del self.LSInstructionsToExecute[i][:]

		del self.instructionsToDecode[:]

	def printRegisters(self, forced=False):
		if self.arguments.step or forced:
			print "\n"
			for idx, register in enumerate(self.registers):
				print "R" + str(idx) + "=" + str(register) + ", "
			print "\n"

	def printMemory(self, forced=False):
		if self.arguments.step or forced:
			self.memory.printMemory()

	def printStats(self):
		print "Finished executing. Stats:"
		print "---------------------------"
		print "Cycles: " + str(self.clockCycles)
		print "Instructions executed: " + str(self.instructionsExecuted)
		print "Cycles per instruction: " + str(self.clockCycles/self.instructionsExecuted)
		print "Stalls: " + str(self.stalls)

###################################################
## FETCH STAGE
###################################################

	def fetch(self, unitID):
		# If we've reached the end of the program, there's nothing else to fetch
		if self.pc >= len(self.program.instructions):
			if self.arguments.step:
				print "FETCH STAGE " + str(unitID) + ": All instructions have been fetched"
			return False
		
		# Check how full the decode buffer is
		if len(self.instructionsToDecode) > config.NUMBER_EXECUTION_UNITS:
			if self.arguments.step:
				print "FETCH STAGE " + str(unitID) + ": Decode buffer full"
			return False

		# Fetch the instruction
		instruction = self.program.instructions[self.pc]
		if self.arguments.step:
			print "FETCH STAGE " + str(unitID) + ": " + str(instruction)
		self.instructionsToDecode.append(instruction)
		self.pc += 1
	
		return True


###################################################
## DECODE STAGE
###################################################

	def decode(self, unitID):
		# If there are no instructions that can be decoded, just return
		if len(self.instructionsToDecode) == 0:
			if self.arguments.step:
				print "DECODE STAGE " + str(unitID) + ": No Instructions in Queue"
			return

		instructionToDecode = self.instructionsToDecode[0]
		if self.arguments.step:
			print "DECODE STAGE " + str(unitID) + ": Decoding instruction " + str(instructionToDecode)

		decodedInstruction = instructionToDecode.decode(self)

		if decodedInstruction.opcode == 'HALT' and self.checkForEmptyQueues(decodeIncluded=False) == False:
			print "DECODE STAGE " + str(unitID) + ": Can't deal with HALT just yet"
			self.stalls += 1
			return 

		blockingInstruction = None

		# Check against LS Units
		for i in range(config.NUMBER_EXECUTION_UNITS):
			checkBlocking = self.dependenciesExist(self.LSInstructionsToExecute[i], decodedInstruction)

			if checkBlocking != None:
				blockingInstruction = checkBlocking
				break

		# Check against ALU units
		if blockingInstruction == None:
			for i in range(config.NUMBER_EXECUTION_UNITS):
				checkBlocking = self.dependenciesExist(self.ALUInstructionsToExecute[i], decodedInstruction)

				if checkBlocking != None:
					blockingInstruction = checkBlocking
					break

		# Check against writeback
		if blockingInstruction == None:
			checkBlocking = self.dependenciesExist(self.instructionsToWriteback, decodedInstruction)
			if checkBlocking != None:
				blockingInstruction = checkBlocking

		# Handle the branch instructions
		if decodedInstruction.instructionType == InstructionType.BRANCH:	
			if blockingInstruction == None:
				# We've just branched, we don't want to decode again
				if self.branchExecutionUnit.execute(decodedInstruction) == True:
					return False
				else:
					self.instructionsToDecode.pop(0)
					return True
			else:
				# Try a branch prediction
				if self.arguments.branchpredictor == True:
					self.branchExecutionUnit.predictedExecution(decodedInstruction, blockingInstruction)

		# If we're not blocked
		if blockingInstruction == None:				
			if decodedInstruction.instructionType == InstructionType.ALU:
				self.ALUInstructionsToExecute[unitID].append(decodedInstruction)
				self.instructionsToDecode.pop(0)
				return True
			elif decodedInstruction.instructionType == InstructionType.MEMORY or \
				 decodedInstruction.instructionType == InstructionType.OTHER:
				self.LSInstructionsToExecute[unitID].append(decodedInstruction)
				self.instructionsToDecode.pop(0)
				return True
			else:
				raise Exception("Unknown instruction type")
		else:
			if self.arguments.step:
				print "DECODE STAGE " + str(unitID) + ": Dependencies exist, stalling" 
			self.stalls += 1
		
		return False

	def dependenciesExist(self, instructionBuffer, instruction):

		sourceRegister1 = instruction.getOperand(1)
		sourceRegister2 = instruction.getOperand(2)

		if instruction.opcode == 'STR':
			sourceRegister1 = instruction.getOperand(0)

		for innerInstruction in instructionBuffer:
			if innerInstruction is None:
				continue

			if innerInstruction.destinationRegister == None:
				continue

			if (sourceRegister1 != None and \
				sourceRegister1.value == innerInstruction.destinationRegister and \
				sourceRegister1.type == OperandType.REGISTER) or \
				(sourceRegister2 != None and \
				sourceRegister2.value == innerInstruction.destinationRegister and \
				sourceRegister2.type == OperandType.REGISTER):
					return innerInstruction

		return None

###################################################
## EXECUTE STAGE
###################################################

	def execute(self):
		# Call execute() on LS and ALU units
		for i in range(config.NUMBER_EXECUTION_UNITS):
			self.ALUExecutionUnits[i].execute()
			self.LSExecutionUnits[i].execute()

###################################################
## WRITEBACK STAGE
###################################################

	def writeBack(self):
		self.writebackUnit.writeback()
