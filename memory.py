from config import *
import sys

class Memory:

	def __init__(self):
		self.reset()

	def load(self, address):
		if address < 0 or address >= len(self.data):
			raise Exception("Access violation at " + str(address))

		return self.data[address]

	def store(self, address, value):
		if address < 0 or address >= len(self.data):
			raise Exception("Access violation at " + str(address))

		self.data[address] = value

	def printMemory(self):
		for i in self.data:
			sys.stdout.write(str(i) + " ")
		print		

	def reset(self):
		self.data = [0] * pow(2, ARCH)
