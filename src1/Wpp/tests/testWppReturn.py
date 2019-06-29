import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppReturn(unittest.TestCase):
	def testAdd(self):
		source = """
func myAdd: double
	param x: double
	param y: double
	x + y
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		# Check isAutoChange for last command in block
		myAddOver = module.dictionary['myAdd']
		self.assertEqual(myAddOver.type, 'Overloads')
		myAddFn = myAddOver.items[0]
		self.assertEqual(myAddFn.type, 'Func')
		block = myAddFn.getBody()
		self.assertEqual(block.type, 'Block')
		lastCmd = block.items[-1]
		self.assertEqual(lastCmd.type, 'Return')
		self.assertTrue(lastCmd.isAutoChange)

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testWithReplace(self):
		source = """
func myMul: double
	param x: double
	param y: double
	return x * y
		"""
		dst = """
func myMul: double
	param x: double
	param y: double
	x * y
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		myMulOver = module.dictionary['myMul']
		self.assertEqual(myMulOver.type, 'Overloads')
		myMulFn = myMulOver.items[0]
		self.assertEqual(myMulFn.type, 'Func')
		block = myMulFn.getBody()
		lastCmd = block.items[-1]
		self.assertEqual(lastCmd.type, 'Return')
		self.assertTrue(lastCmd.isAutoChange) # Т.к. при экспорте return не выводится
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(dst))
