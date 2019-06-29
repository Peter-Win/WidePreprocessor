import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestWppConst(unittest.TestCase):
	def testSimple(self):
		source = """
var public year: int = 2019
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInvalidType(self):
		source = """
var public year: int = 3.14
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "3.14:float" to "int"')

	def testInvalidUnsigned(self):
		source = """
var public size: unsigned int = -1
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Conversion from "-1" to "unsigned int"')

	def testNull(self):
		source = """
class public A
var public inst: A = null
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))
