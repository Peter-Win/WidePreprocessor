import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestMemberAccess(unittest.TestCase):
	def testThis(self):
		source = """
class A
	method getInstance: A
		return this
"""
		module = WppCore.createMemModule(source, 'this.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testField(self):
		source = """
class public Abc
	field value: double
	method const getValue: double
		return this.value
"""
		module = WppCore.createMemModule(source, 'field.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testWrongField(self):
		source = """
class Hello
	field public value: double = 1
var h: Hello = Hello()
var value: double = h.value
var wrong: double = h.wrong
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'wrongField.wpp')
		self.assertEqual(cm.exception.args[0], '"Hello" class has no member "wrong"')
		self.assertEqual(cm.exception.args[1], ('wrongField.wpp', 6, 'var wrong: double = h.wrong'))

	def testProtectedError(self):
		source = """
class Stub
	field protected value: double = 1
var a: Stub = Stub()
var v: double = a.value
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'protectedError.wpp')
		self.assertEqual(cm.exception.args[0], 'Member "value" is protected and only accesible within class "Stub" and its subclasses')
		self.assertEqual(cm.exception.args[1], ('protectedError.wpp', 5, 'var v: double = a.value'))

	def testPrivateError(self):
		source = """
class Parent
	field private value: int = 1
var p: Parent = Parent()
var v: int = p.value
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'privateError.wpp')
		self.assertEqual(cm.exception.args[0], 'Member "value" is private and only accesible within class "Parent"')
		self.assertEqual(cm.exception.args[1], ('privateError.wpp', 5, 'var v: int = p.value'))

	def testPrivateError2(self):
		source = """
class Parent
	field private value: int = 1
class Child
	extends Parent
	method getValue: int
		return value
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'privateError2.wpp')
		self.assertEqual(cm.exception.args[0], 'Member "value" is private and only accesible within class "Parent"')
		self.assertEqual(cm.exception.args[1], ('privateError2.wpp', 7, '\t\treturn value'))
