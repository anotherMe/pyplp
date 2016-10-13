#!/usr/bin/python3

import os
import unittest
import parsers


def silentremove(filename):
	"""Remove given filename if exists. Fails silently.
	"""
	try:
		os.remove(filename)
	except OSError:
		pass
		

class Line_test(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def tearDown(self):	
		pass

	def test_removeFirst(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		line.removeFirst(19)
		self.assertEqual(line.len(), 27)
		
	def test_cutAt(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		tVal = line.cutAt(29) # cut at ħ character
		self.assertEqual(tVal, "]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ")
		
		
	def test_cutAtFirst(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		line.cutAtFirst('ħ')
		self.assertEqual(line.get(), "{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")



if __name__ == '__main__':
	
	unittest.main()
