#!/usr/bin/env python

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

	def test_remove_1(self):
		line = parsers.Line("Abracadabra, open sesame")
		line.remove("Abracadabra, ")
		self.assertEqual(line.get(), "open sesame")

	def test_remove_2(self):
		line = parsers.Line("Abracadabra, open sesame")
		self.assertRaises(parsers.CutException, line.remove, "Accabadora, ")

	def test_removeFirst(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		line.removeFirst(19)
		self.assertEqual(line.len(), 27)
		
	def test_cutAtPos(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		tVal = line.cutAtPos(29) # cut at ħ character
		self.assertEqual(tVal, "]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ")
		
		
	def test_cutAt(self):
		
		line = parsers.Line("]ĸ²¶ĸ]}eoyvuy4yyn758nv7854]ĸħ{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")
		line.cutAt('ħ')
		self.assertEqual(line.get(), "{ĸ¢}³¼]ĸ²¶ĸ]}`ð²ĸ")



if __name__ == '__main__':
	
	unittest.main()
