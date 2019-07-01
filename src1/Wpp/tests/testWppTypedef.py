import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppTypedef(unittest.TestCase):
	def testInModule(self):
		source = """
typedef public TSize: unsigned long
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInClass(self):
		source = """
class public MyClass:
	typedef public TSize: unsigned long
		"""
		module = WppCore.createMemModule(source, 'MyClass.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInBlock(self):
		source = """
func public main
	typedef TSize: unsigned long
	var x: TSize = 1
		"""
		module = WppCore.createMemModule(source, 'main.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInvalidMatch(self):
		source = """
func public main
	typedef TSize: unsigned long
	var x: TSize = 1.1
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "1.1:float" to "TSize"')
