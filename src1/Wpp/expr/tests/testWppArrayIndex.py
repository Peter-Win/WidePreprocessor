import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppArrayIndex(unittest.TestCase):
	def testRightOk(self):
		source = """
func public main
	var values: Array double = [0.1, 0.2, -3.3]
	var first: double = values[0]
	var last: double = values[values.length - 1]
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testLeftOk(self):
		source = """
func public main
	var values: Array double = [0.1, 0.2, -3.3]
	values[1] = values[0]
	values[values.length - 1] = 3.14
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testBadIndex(self):
		""" It is wrong to use 0.1 as index in construction values[0.1] """
		source = """
func public main
	var values: Array double = [0.1, 0.2, -3.3]
	var d: double = values[0.1]
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		# self.assertEqual(cm.exception.args[0], 'Cant match call of WppCore.-(unsigned long; 1.1)')

	def testBadItemType(self):
		source = """
func public main
	var values: Array int = [1, 2, 4]
	values[1] = 2.2
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
