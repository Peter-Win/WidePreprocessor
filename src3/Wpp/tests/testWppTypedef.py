import unittest
from Wpp.WppTypedef import WppTypedef
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

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

	def testComment(self):
		source = """
typedef public Size = unsigned long
	# First comment line.
	# Second line.
"""
		module = WppCore.createMemModule(source, "comment.wpp")
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())

	def testInvalidName(self):
		source = 'typedef public myType = unsigned int'
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'invalidName.wpp')
		self.assertEqual(cm.exception.args[0], 'UpperCamelCase is required for typedef name "myType"')

