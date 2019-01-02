import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppCall(unittest.TestCase):
	def testCallFunc(self):
		source = """
func public first: double
	param x: double
	param y: double
	x * x + y

func public second: double
	param a: double
	param b: double
	first(a + 1, b)
		"""
		module = WppCore.createMemModule(source, 'callFunc.fake')
		secondOver = module.dictionary['second']
		self.assertEqual(secondOver.type, 'Overloads')
		secondFunc = secondOver.items[0]
		self.assertEqual(secondFunc.type, 'Func')
		cmd = secondFunc.getBody().items[-1]
		self.assertEqual(cmd.type, 'Return')
		expr = cmd.getExpression()
		self.assertEqual(expr.type, 'Call')
		caller = expr.getCaller()
		self.assertEqual(caller.type, 'IdExpr')
		self.assertEqual(caller.id, 'first')
		args = expr.getArguments()
		self.assertEqual(len(args), 2)

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testCallMethod(self):
		source = """
class public CallMethod
	method public square: double
		param x: double
		x * x
	method public lengthSqr: double
		param x: double
		param y: double
		square(x) + square(y)
		"""
		module = WppCore.createMemModule(source, 'CallMetod.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
