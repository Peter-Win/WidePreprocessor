import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppCore(unittest.TestCase):
	def testLength(self):
		source = """
func test: String
	param value: String
	value.length == 0 ? "Empty" : "Full"
		"""
		module = WppCore.createMemModule(source, 'length.fake')
		funcOver = module.dictionary['test']
		func = funcOver.items[0]
		cmd = func.getBody().items[0]
		self.assertEqual(cmd.type, 'Return')
		expr = cmd.getExpression()
		self.assertEqual(expr.type, 'TernaryOp')
		cond = expr.getCondition()
		self.assertEqual(cond.type, 'BinOp')
		self.assertEqual(cond.opCode, '==')
		pt = cond.getLeft()
		self.assertEqual(pt.type, 'BinOp')
		self.assertEqual(pt.opCode, '.')
		length = pt.getRight()
		self.assertEqual(length.type, 'FieldExpr')
		self.assertEqual(length.id, 'length')
		lengthDecl = length.getDeclaration()
		self.assertEqual(lengthDecl.type, 'Field')
		self.assertEqual(lengthDecl.cloneScheme, 'Owner')
		self.assertEqual(lengthDecl.owner.type, 'Class')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())