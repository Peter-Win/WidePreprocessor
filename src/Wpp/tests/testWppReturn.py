import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemory import OutContextMemory

class TestWppReturn(unittest.TestCase):
	def testReturnVoid(self):
		source = """
func empty
	return
		"""
		module = WppCore.createMemModule(source, 'empty.fake')
		over = module.dictionary['empty']
		func = over.items[0]
		block = func.getBody()
		ret = block.items[0]
		self.assertEqual(ret.type, 'Return')
		self.assertIsNone(ret.getExpression())

	def testReturnExpr(self):
		module = WppCore.createMemModule("func intTest: int\n\treturn 21", 'intTest.fake')
		over = module.items[0]
		func = over.items[0]
		block = func.getBody()
		ret = block.items[0]
		self.assertEqual(ret.type, 'Return')
		expr = ret.getExpression()
		self.assertIsNotNone(expr)
		self.assertEqual(expr.type, 'Const')
		self.assertEqual(expr.exportString(), '21')

	def testAutoChange(self):
		source = """
func autoChange: int
	param x: int
	x + 1
		"""
		module = WppCore.createMemModule(source, 'autoChange.fake')
		over = module.items[0]
		func = over.items[0]
		block = func.getBody()
		ret = block.items[0]
		self.assertEqual(ret.type, 'Return')
		self.assertEqual(ret.isAutoChange, True)
		expr = ret.getExpression()
		self.assertIsNotNone(expr)
		self.assertEqual(expr.type, 'BinOp')
		self.assertEqual(expr.exportString(), 'x + 1')

		outContext = OutContextMemory()
		func.export(outContext)
		self.assertEqual(str(outContext), source.strip())
