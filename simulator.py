from processor import Processor
from assembler import Assembler
from instructionBuffer import InstructionBuffer
from memory import Memory

import argparse

class Simulator():

	def __init__(self, args):
		self.args = args
		self.memory = Memory()

	def run(self):
		self.assembledProgram = Assembler(self.memory, args)
		self.processor = Processor(self, self.memory, args)
		self.processor.run(self.assembledProgram)
	
if __name__ == '__main__':
	# Parse the command line options
	parser = argparse.ArgumentParser(description="A Processor Simulator")
	parser.add_argument('-s','--step', action="store_true", help='Whether to step through the program', default=False)
	parser.add_argument('-f','--file', help="The file to execute", required=True)
	args = parser.parse_args()

	# Load the file
	simulator = Simulator(args)
	simulator.run()
