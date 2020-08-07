import unittest
from Wpp.WppExpression import WppExpression, WppConst, WppNamed, WppCall
from Wpp.Context import Context

class TestWppExpression(unittest.TestCase):
	def testParseInt(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('-123', ctx)
		self.assertEqual(expr.type, WppConst.type)
		self.assertEqual(expr.constType, 'int')

	def testParseBool(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('true', ctx)
		self.assertEqual(expr.type, WppConst.type)
		self.assertEqual(expr.constType, 'bool')

	def testParseNamed(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('myName', ctx)
		self.assertEqual(expr.type, WppNamed.type)
		self.assertEqual(expr.targetName, 'myName')

	def testParseCall0(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('myFunc()', ctx)
		self.assertEqual(expr.type, WppCall.type)
		caller = expr.getCaller()
		self.assertEqual(caller.type, WppNamed.type)
		args = expr.getArguments()
		self.assertEqual(args, [])

	def testParseCall3(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('myFunc3(x, 3.14, false)', ctx)
		self.assertEqual(expr.type, WppCall.type)
		caller = expr.getCaller()
		self.assertEqual(caller.type, WppNamed.type)
		args = expr.getArguments()
		self.assertEqual(len(args), 3)
		self.assertEqual(args[0].type, WppNamed.type)
		self.assertEqual(args[1].type, WppConst.type)
		self.assertEqual(args[1].constType, 'fixed')
		self.assertEqual(args[2].type, WppConst.type)
		self.assertEqual(args[2].constType, 'bool')

	def testParseCallNested(self):
		ctx = Context.createFromMemory('')
		expr = WppExpression.parse('func1(func2(x, 100), func3(y, 200))', ctx)
		self.assertEqual(expr.type, WppCall.type)
		caller = expr.getCaller()
		self.assertEqual(caller.type, WppNamed.type)
		self.assertEqual(caller.targetName, 'func1')
		args = expr.getArguments()
		self.assertEqual(len(args), 2)
		self.assertEqual(args[0].type, WppCall.type)
		self.assertEqual(args[1].type, WppCall.type)
		self.assertEqual(args[0].getCaller().targetName, 'func2')
		self.assertEqual(args[1].getCaller().targetName, 'func3')
		self.assertEqual(expr.buildQuasiType(), None)
