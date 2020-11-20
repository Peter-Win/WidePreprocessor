import unittest
from Wpp.WppCore import WppCore
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSModule(unittest.TestCase):
	def testClone(self):
		srcModule = WppCore.createMemModule('', 'number.mem')
		self.assertEqual(srcModule.type, 'module')
		self.assertEqual(srcModule.getName(), 'number')

		dstCore = TSCore.createInstance()
		dstModule = srcModule.cloneAll(dstCore)
		self.assertEqual(dstModule.type, 'module')
		self.assertEqual(dstModule.getName(), 'number_')
		self.assertTrue(dstModule.isModule())

	def testSimple(self):
		tsModule = TSCore.createModuleFromWpp("var public const pi: double = 3.14", 'module.wpp')
		self.assertEqual(tsModule.type, 'module')
		self.assertEqual(len(tsModule.items), 1)
		txVarDecl = tsModule.items[0]
		self.assertEqual(txVarDecl.type, 'var')
		self.assertIn('hiddenType', txVarDecl.attrs)
		txTypeExpr = txVarDecl.getTypeTaxon()
		self.assertEqual(txTypeExpr.type, '@typeExprName')
		txType = txTypeExpr.getTypeTaxon()
		self.assertEqual(txType.type, 'scalar')
		self.assertEqual(txType.getName(), 'number')	# 'double' in TS translated to 'number'

		txVal = txVarDecl.getValueTaxon()
		self.assertIsNot(txVal, None)
		self.assertEqual(txVal.type, 'const')

		code = tsModule.exportText(style)[0]
		self.assertEqual(code, 'export const pi = 3.14;')

	def testComment(self):
		source = """
# Header comment.
# Second header line.
var public const isActive: bool = true
"""
		expected = """
// Header comment.
// Second header line.
export const isActive = true;
"""
		tsModule = TSCore.createModuleFromWpp(source, 'comment.wpp')
		ctx = OutContextMemoryStream()
		tsModule.exportContext(ctx, style)
		self.assertEqual(str(ctx), expected.strip())
