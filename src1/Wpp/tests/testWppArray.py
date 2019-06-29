import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppArrayIndex(unittest.TestCase):
	def testLengthOk(self):
		source = """
func public main
	var values: Array double = [0.1, 0.2, -3.3]
	var valuesSize: unsigned long = values.length
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testLengthInvalidType(self):
		source = """
func public main
	var values: Array double = [0.1, 0.2, -3.3]
	var valuesSize: double = values.length
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "values.length:unsigned long" to "double"')

	def testPushPopOk(self):
		source = """
func public main
	var values: Array double
	values.push(3.14)
	var pi: double = values.pop()
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))


