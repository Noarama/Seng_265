#!/usr/bin/env python
# Author: Noa Arama


import random

class ArtConfig:

	def __init__(self):
		'''ArtConfig initilizer'''
		self.shape = random.randint(0,3)
		self.xcord = random.randint(0,501)
		self.ycord = random.randint(0, 301)
		self.cirRad = random.randint(0, 100)
		self.eliSRad = random.randint(10,30)
		self.eliRad = random.randint(10,30)
		self.rectWidth = random.randint(10,100)
		self.rectHeight = random.randint(10,100)
		self.red = random.randint(0,255)
		self.green = random.randint(0,255)
		self.blue = random.randint(0,255)
		self.opa = random.random()

	def printLine(self,count):
		'''printLine method'''
		print(f"{count: <5}{self.shape: <5}{self.xcord: <5}{self.ycord: <5}{self.cirRad: <5}{self.eliSRad: <5}{self.eliRad: <5}{self.rectWidth: <5}{self.rectHeight: <5}{self.red: <5}{self.green: <5}{self.blue: <5}{self.opa: .1f}")

def main() -> None:
	"""main method"""
	i = 0
	# below prints titles of table
	titles = ["CNT" , "SHA" , "X" , "Y" , "RAD" , "RX" , "RY" , "W" , "H" , "R" , "G" , "B" , "OP"]
	print(f"{titles[0]: <5}{titles[1]: <5}{titles[2]: <5}{titles[3]: <5}{titles[4]: <5}{titles[5]: <5}{titles[6]: <5}{titles[7]: <5}{titles[8]: <5}{titles[9]: <5}{titles[10]: <5}{titles[11]: <7}{titles[12]: <12}")
	
	# Prints 10 lines of random numbers 
	while i < 10:
		s1 = ArtConfig()
		s1.printLine(i)
		i = i+1



if __name__ == "__main__":
    main()

