import unittest
from Wpp.WppCore import WppCore
from Wpp.WppExpression import WppExpression
from Wpp.Context import Context
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppSuper(unittest.TestCase):
	def testParse(self):
		source = 'super(1)'
		ctx = Context.createFromMemory(source, 'parseSuper.wpp')
		expr = WppExpression.parse(source, ctx)
		self.assertEqual(expr.type, 'call')
		caller = expr.getCaller()
		self.assertEqual(caller.type, 'super')

	def testConstructor(self):
		source = """
class Parent
	field first: int
	constructor
		autoinit first
class Child
	extends Parent
	field second: double
	constructor
		param first: int
		autoinit second
		super(first)
"""
		module = WppCore.createMemModule(source, 'superCon.wpp')

		Child = module.findItem('Child')
		con = Child.findConstructor()
		body = con.getBody()
		txSuper = body.items[0].getCaller()
		self.assertEqual(txSuper.type, 'super')
		self.assertTrue(txSuper.isConstructor())
		self.assertFalse(txSuper.isOverride())

		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testVirtual(self):
		source = """
class First
	method virtual getId: int
		return 1
class Second
	extends First
	method override getId: int
		return super() + 1
var obj: First = Second()
var v: int = obj.getId()
"""
		module = WppCore.createMemModule(source, 'superCon.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
