#!/usr/bin/python3

import pdb

class CutException(Exception):
	pass


class Line:
	
	def __init__ (self, line):
		
		self.line = line

	def len(self):
		"""Return actual line string length"""
		
		return len(self.line)
		
	def readFirst(self, num):
		"""	Return first num characters. Just read, no actual modification 
			on the line string.
		"""
		
		return self.line[:num]
		
	def get(self):
		"""Return actual line string"""
		
		return self.line

	def removeFirst(self, num):
		"""Remove first <num> characters

			Arguments:
			num -- number of characters to remove
			
			Returns nothing
		"""	
		
		self.line = self.line[num:]
	
	
	def cutAt(self, position):
		"""Cut line at given position

			Arguments:
			position -- count starts at 1
			
			Returns line from position 1 to given position (included).
		"""	
		
		val = self.line[:position]
		self.line = self.line[position:]
		return val
		
		
	def cutAtFirst(self, character):
		"""Cut line at first occurrence of character

			Arguments:
			character -- search stops at first occurrence
			
			Returns string before given character position
		"""	
		
		if self.line.find(character) < 0:
			raise CutException('Character not found')
		
		val = self.line[:self.line.find(character)]
		self.line = self.line[self.line.find(character)+1:]
		return val