import unittest
from Wpp.WppTypedef import WppTypedef
from Wpp.WppCore import WppCore

class TestWppTypedef(unittest.TestCase):
	def testParse(self):
		errMsg, name, attrs, expr = WppTypedef.parse('typedef public Size = unsigned long')
		self.assertIsNone(errMsg)
		self.assertEqual(name, 'Size')
		self.assertEqual(attrs, {'public'})
		self.assertEqual(expr, 'unsigned long')

	def testUsing(self):
		source = """
typedef public Size = unsigned long
var public const width: Size = 12345
"""
		module = WppCore.createMemModule(source, "using.wpp")
		self.assertEqual(len(module.items), 2)
		txSize = module.findItem('Size')
		self.assertIsInstance(txSize, WppTypedef)
		txTypeExpr = txSize.getTypeExpr()
		self.assertEqual(txTypeExpr.attrs, {'unsigned'})
		qt = txSize.buildQuasiType()
		self.assertEqual(qt.attrs, {'unsigned'})

