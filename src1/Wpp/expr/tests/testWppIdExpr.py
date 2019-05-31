import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream


class TestWppIdExpr(unittest.TestCase):
	def testVar(self):
		source = """
var valueF: float = 1.11
var public valueD: double = valueF
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInvalidType(self):
		source = """
var valueF: float = 1.11
var public valueL: long = valueF
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "valueF:IdExpr" to "long"')
