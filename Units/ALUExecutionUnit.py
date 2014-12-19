class ALUExecutionUnit():

	def __init__(self, processor, unitID):
		self.processor = processor
		self.ID = unitID
		self.currentInstruction = None
		self.cycles = 0

	def execute(self):

		# Get the instructions
		instructions = self.processor.ALUInstructionsToExecute[self.ID]
		if len(instructions) == 0 and self.currentInstruction is None:
			if self.processor.arguments.step:
				print "ALU UNIT" + str(self.ID) + ": No instructions to execute"
			return

		# Get the next Instruction
		if self.currentInstruction == None:
			self.currentInstruction = instructions[0]

		self.cycles += 1

		# Only execute when the simulated cycles have been done
		if self.cycles < self.currentInstruction.latency:
			if self.processor.arguments.step:
				print "ALU UNIT" + str(self.ID) + ": Executing instruction " + str(self.currentInstruction) + self.getCycleStats()
			
		if self.cycles == self.currentInstruction.latency:
			if self.processor.arguments.step:
				print "ALU UNIT" + str(self.ID) + ": Executing instruction " + str(self.currentInstruction)
			if self.currentInstruction in self.processor.ALUInstructionsToExecute[self.ID]:
				self.processor.ALUInstructionsToExecute[self.ID].remove(self.currentInstruction)
			# And execute it
			self.currentInstruction.execute(self.processor)
			# Add it to writeback
			self.processor.instructionsToWriteback.append(self.currentInstruction)

			# Reset the execution unit
			self.cycles = 0
			self.currentInstruction = None

			# Add another instruction executed to the processor stats
			self.processor.instructionsExecuted += 1
		
	def getCycleStats(self):
		cycleStats = " (" + str(self.cycles) + "/" + str(self.currentInstruction.latency) + ")"
		return cycleStats