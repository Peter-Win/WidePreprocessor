import unittest
from Wpp.WppCore import WppCore
from core.ErrorTaxon import ErrorTaxon

class TestWppBody(unittest.TestCase):

	def testDuplicate(self):
		source = """
func public myFunc: double
	var abcd: double = 123
	var abcd: int = -1
	return abcd
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'dup.mem')
		self.assertEqual(cm.exception.args[0], 'Duplicate identifier "abcd"')
