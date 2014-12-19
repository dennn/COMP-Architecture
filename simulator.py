from processor import Processor
from assembler import Assembler
from memory import Memory
import config

import argparse

class Simulator():

	def __init__(self, args):
		self.args = args
		self.memory = Memory()
		if self.args.exeUnits:
			config.NUMBER_EXECUTION_UNITS = int(args.exeUnits)

		if self.args.step:
			print "Executing " + str(self.args.file) + " with " + str(config.NUMBER_EXECUTION_UNITS) + " execution units"

	def run(self):
		self.assembledProgram = Assembler(self.memory, args)
		self.processor = Processor(self.memory, args)
		self.processor.run(self.assembledProgram)
	
if __name__ == '__main__':
	# Parse the command line options
	parser = argparse.ArgumentParser(description="A Processor Simulator")
	parser.add_argument('-s','--step', action="store_true", help='Whether to step through the program', default=False)
	parser.add_argument('-f','--file', help="The file to execute", required=True)
	parser.add_argument('-e', '--exeUnits', type=int, help="The number of execution units")
	parser.add_argument('-b', '--branchpredictor', action="store_true", help="Whether to turn on branch prediction", default=False)
	args = parser.parse_args()

	# Load the file
	simulator = Simulator(args)
	simulator.run()
