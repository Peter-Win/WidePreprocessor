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
	method square: double
		param x: double
		x * x
	method lengthSqr: double
		param x: double
		param y: double
		square(x) + square(y)
		"""
		module = WppCore.createMemModule(source, 'CallMetod.fake')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testCallMethodStatic(self):
		source = """
class static MyMath
	method abs: double
		param value: double
		value < 0.0 ? -value : value

func public main
	var x: double = MyMath.abs(-3.14)
		"""
		module = WppCore.createMemModule(source, 'CallMetod.fake')
		classMyMath = module.dictionary['MyMath']
		self.assertIn('static', classMyMath.attrs)
		absOver = classMyMath.dictionary['abs']
		absMethod = absOver.items[0]
		self.assertEqual(absOver.type, 'Overloads')
		self.assertEqual(absMethod.type, 'Method')
		self.assertTrue(absMethod.canBeStatic)
		self.assertIn('static', absMethod.attrs)
		self.assertIn('static', absOver.attrs)

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testNew(self):
		source = """
class Hello
	field count: int
	constructor
		param init count
	method static create22: Hello
		Hello(22)
		"""
		module = WppCore.createMemModule(source, 'testNew.fake')
		classHello = module.dictionary['Hello']
		overCreate22 = classHello.dictionary['create22']
		create22 = overCreate22.items[0]
		self.assertEqual(create22.type, 'Method')
		self.assertEqual(create22.name, 'create22')
		cmd = create22.getBody().items[-1]
		self.assertEqual(cmd.type, 'Return')
		expr = cmd.getExpression()
		caller = expr.getCaller()
		self.assertEqual(caller.type, 'IdExpr')
		callerDecl = caller.getDeclaration()
		self.assertEqual(callerDecl, classHello)
		self.assertEqual(expr.type, 'New')
