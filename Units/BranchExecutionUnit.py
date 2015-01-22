# -*- coding: utf-8 -*-
from Instructions.instruction import Instruction
from Instructions.instruction import InstructionType
from Instructions.instruction import OperandType

class BranchExecutionUnit():

	def __init__(self, processor, predictor):
		self.processor = processor
		self.predictor = predictor
		self.predictions = []

	def execute(self, instruction):

		# Add another instruction executed to the processor stats
		self.processor.instructionsExecuted += 1

		if instruction.willTakeBranch(self.processor) == True:
			if self.processor.arguments.step:
				print "BRANCH UNIT: Branching\n"

			# Flush instructions to decode 
			del self.processor.instructionsToDecode[:]

			return True
		else:
			if self.processor.arguments.step:
				print "BRANCH UNIT: Not branching"

		return False

	def predictedExecution(self, instruction, blockingInstruction):
		# Just execute if we have no predictor
		if self.predictor == None:
			raise Exception("No branch predictor initialised")

		# Get the prediction
		branchPrediction = self.predictor.predictBranch(instruction)

		# Change the program counter
		self.processor.pc = branchPrediction.addressToJumpTo
		# Flush instructions to decode
		del self.processor.instructionsToDecode[:]

		# Add another instruction executed to the processor stats
		self.processor.instructionsExecuted += 1

		if self.processor.arguments.step and branchPrediction.shouldTake == True:
			print "Taking branch prediction to " + str(instruction.decodedOperands[0].value.memoryLocation)
		elif self.processor.arguments.step:
			print "BRANCH UNIT: Not taking branch prediction"

		# Create a dictionary
		prediction = { "branchInstruction" : instruction,
					   "branchPrediction" : branchPrediction }

		# Only allow one level of depth
		if len(self.predictions) >= 1:
			return

		self.predictions.append(prediction)
		blockingInstruction.addListener(self)

	def handleWriteback(self, blockingInstruction):
		blockingInstruction.removeListener(self)

		# Get the prediction
		prediction = self.predictions.pop(0)

		branchPrediction = prediction["branchPrediction"]
		branchInstruction = prediction["branchInstruction"]

		#Recalculate the instruction
		newInstruction = Instruction(branchInstruction.rawInstruction, self.processor.program)
		decodedNewInstruction = newInstruction.decode(self.processor)

		# Check if we were right to branch
		if branchPrediction.shouldTake != decodedNewInstruction.shouldBranch():

			# Clear everything
			self.processor.clearAllBuffers()

			# Jump back to the right place
			if branchPrediction.shouldTake == False:
				if self.processor.arguments.step:
					print "Incorrect branch prediction, should have taken"
				self.processor.pc = branchPrediction.failureAddress
			else:
				if self.processor.arguments.step:
					print "Incorrect branch prediction, should not have taken"
				self.processor.pc = branchPrediction.failureAddress
		else:
			if self.processor.arguments.step:
				if branchPrediction.shouldTake == True:
					print "Correct to branch on instruction " +str(blockingInstruction)
				else:
					print "Correct to not branch on instruction " +str(blockingInstruction)