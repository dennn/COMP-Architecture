from processor import Processor
from assembler import Assembler
from instructionBuffer import InstructionBuffer
from fetcher import FetchUnit
from decoder import DecodeUnit
import argparse

class Simulator():

	def __init__(self):
		self.pipelineStages = []
		self.clockCycles = 0
		self.pc = 0
		self.assembledProgram = None
		self.registers = [0] * ARCH
		self.memory = Memory()

	def initPipelineUnits(self):
		self.fetchUnit = FetchUnit(self, self.assembledProgram.instructions)
		self.decodeUnit = DecodeUnit(self)

	def initInstructionBuffer(self):
	#	self.instructionBuffer = InstructionBuffer(self.assembledProgram.instructions)

	def clockCycle(self):
		self.fetchUnit.clockTick()
		self.clockCycles += 1

	def run(self):
		# Parse the command line options
		parser = argparse.ArgumentParser(description="A Processor Simulator")
		parser.add_argument('-s','--step', action="store_true", help='Whether to step through the program', default=False)
		parser.add_argument('-f','--file', help="The file to execute", required=True)
		args = parser.parse_args()

		cpu = Processor(args)
		self.initPipelineUnits()
		self.assembledProgram = Assembler(cpu, args)
		self.initInstructionBuffer()
		#cpu.run(assembler)
	
if __name__ == '__main__':
	Simulator = Simulator()
	Simulator.run()
