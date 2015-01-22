import sys

# A simple static branch predictor
# Follows the same static predictions as the ARM11 processor 
# http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0360f/ch06s02s03.html
class BranchPredictor:

	def __init__(self, processor):
		self.processor = processor

	def predictBranch(self, instruction):
		
		# Current address
		currentInstructionAddress = self.processor.pc

		# Get the address to branch to
		branchAddress = instruction.decodedOperands[0].value.memoryLocation
		failureAddress = currentInstructionAddress + 1

		branchPrediction = None

		if branchAddress > currentInstructionAddress:
			# If it's a forward unconditional, take
			if instruction.opcode == 'B':
				branchPrediction = BranchResult(True, branchAddress, failureAddress)
			# Otherwise don't take
			else:
				branchPrediction = BranchResult(False, failureAddress, branchAddress)
		else:
			# Take all backwards branches
			branchPrediction = BranchResult(True, branchAddress, failureAddress)

		return branchPrediction

class BranchResult:

	def __init__(self, take, addressPredicted, failureAddress):
		self.shouldTake = take
		self.addressToJumpTo = addressPredicted
		self.failureAddress = failureAddress

	def __str__(self):
		if self.shouldTake:
			return "Predicted that we should branch"
		else:
			return "Predicted that we shouldn't branch"