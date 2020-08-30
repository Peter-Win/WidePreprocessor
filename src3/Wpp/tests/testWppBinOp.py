import unittest
from Wpp.WppCore import WppCore

class TestWppBinOp(unittest.TestCase):
	def testArith(self):
		source = """
var const a: double = 1
var const b: double = 2
var const c: double = a * b + 3
var const d: double = (a + b) * c
# var const e: double = a + (b * c)
"""
		module = WppCore.createMemModule(source, 'arith.wpp')
		c = module.findItem('c')
		valC = c.getValueTaxon()
		self.assertEqual(valC.exportString(), 'a * b + 3')
		self.assertEqual(valC.opcode, '+')
		self.assertEqual(valC.getPrior(), 14)

		d = module.findItem('d')
		valD = d.getValueTaxon()
		self.assertEqual(valD.opcode, '*')
		self.assertEqual(valD.exportString(), '(a + b) * c')

