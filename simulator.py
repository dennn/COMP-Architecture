from processor import Processor
from assembler import Assembler
from instructionBuffer import InstructionBuffer
from fetcher import FetchUnit
from decoder import DecodeUnit
import argparse

class Simulator():

	def __init__(self, args):
		self.args = args
		self.initProcessor()
		self.initPipelineUnits()

	def initProcessor(self):
		self.assembledProgram = None
		self.clockCycles = 0
		self.pc = 0
		self.memory = Memory()
		self.registers = [0] * ARCH

	def initPipelineUnits(self):
		self.fetchUnit = FetchUnit(self, self.assembledProgram.instructions)
		self.decodeUnit = DecodeUnit(self)

	def clockCycle(self):
		self.fetchUnit.clockTick()
		self.clockCycles += 1

	def run(self):
		cpu = Processor(args)
		self.initPipelineUnits()
		self.assembledProgram = Assembler(cpu, args)
		self.initInstructionBuffer()
	
if __name__ == '__main__':
	# Parse the command line options
	parser = argparse.ArgumentParser(description="A Processor Simulator")
	parser.add_argument('-s','--step', action="store_true", help='Whether to step through the program', default=False)
	parser.add_argument('-f','--file', help="The file to execute", required=True)
	args = parser.parse_args()

	# Load the file
	simulator = Simulator(args)
	simulator.run()
