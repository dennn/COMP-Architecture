# -*- coding: utf-8 -*-

class WriteBackUnit():

	def __init__(self, processor):
		self.processor = processor

	def writeback(self):

		# Get the instructions
		instructions = self.processor.instructionsToWriteback
		if len(instructions) == 0:
			if self.processor.arguments.step:
				print "WRITEBACK STAGE: No Instructions to writeback"
			return

		# Write back any instructions that exist in the queue
		for instruction in instructions:
			instruction.instructionStage = 'WB'
			if self.processor.arguments.step:
				print "WRITEBACK STAGE: Writing back instruction " + str(instruction)
			instruction.writeback(self.processor)

		del self.processor.instructionsToWriteback[:]

		
