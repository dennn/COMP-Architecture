from processor import Processor
from assembler import Assembler
import argparse

def main():
	# Parse the command line options
	parser = argparse.ArgumentParser(description="A Processor Simulator")
	parser.add_argument('-s','--step', action="store_true", help='Whether to step through the program', default=False)
	parser.add_argument('-f','--file', help="The file to execute", required=True)
	args = parser.parse_args()

	cpu = Processor(args)
	assembler = Assembler(cpu, args)
	cpu.run(assembler)

if __name__ == '__main__':
	main()