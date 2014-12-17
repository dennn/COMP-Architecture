class BranchExecutionUnit():

	def __init__(self, processor):
		self.processor = processor

	def execute(self, instruction):

		# Add another instruction executed to the processor stats
		self.processor.instructionsExecuted += 1

		if instruction.willTakeBranch(self.processor) == True:
			if self.processor.arguments.step:
				print "BRANCH UNIT: Branching\n"

			# Flush all the buffers
			del self.processor.instructionsToDecode[:]

			return True

		return False