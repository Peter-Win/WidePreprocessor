import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestWppMethod(unittest.TestCase):
	def testWrongOverload(self):
		source = """
class Value
	field x: double = 0
	method add: double
		param value: double
		return x + value
	method add: double
		param v: Value
		return x + v.x
"""
		with self.assertRaises(RuntimeError) as cm:		
			module = WppCore.createMemModule(source, 'wrongOverload.wpp')
		msg = cm.exception.args[0]
		self.assertEqual(msg, 'Use "overload" attribute for "add"')


	def testOverload(self):
		source = """
class Value
	field x: double = 0
	method overload add: double
		param value: double
		return x + value
	method overload add: double
		param v: Value
		return x + v.x
"""
		module = WppCore.createMemModule(source, 'overload.wpp')
		Value = module.findItem('Value')
		add = Value.findItem('add')
		self.assertEqual(add.type, 'overload')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testDupField(self):
		source = """
class Parent
	field myMember: int = 1
class Child
	extends Parent
	method myMember: int
		return 2
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'dupField.wpp')
		self.assertEqual(cm.exception.args[0], 'Parent class "Parent" already has a field "myMember"')
		self.assertEqual(cm.exception.args[1], ('dupField.wpp', 6, '\tmethod myMember: int'))

	def testNoAttrOverride(self):
		source = """
class Parent
	method virtual getId: int
		return 1
class Child
	extends Parent
	method getId: int
		return 2
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'noAttrOverride.wpp')
		self.assertEqual(cm.exception.args[0], 'Parent class "Parent" already has a method "getId". Attribute "override" must be used.')
		self.assertEqual(cm.exception.args[1], ('noAttrOverride.wpp', 7, '\tmethod getId: int'))

	def testNoAttrVirtual(self):
		source = """
class Parent
	method getId: int
		return 1
class Child
	extends Parent
	method override getId: int
		return 2
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'noAttrVirtual.wpp')
		self.assertEqual(cm.exception.args[0], 'Parent class "Parent" already has a non-virtual method "getId"')

	def testWrongOverride1(self):
		source = """
class Parent
	method override getId: int
		return 1
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'wrongOverride.wpp')
		self.assertEqual(cm.exception.args[0], 'The overridden function can only be in derived class')

	def testWrongOverride2(self):
		source = """
class Parent
	method virtual getId: int
		return 1
class Child
	extends Parent
	method override second: int
		return 2
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'wrongOverride.wpp')
		self.assertEqual(cm.exception.args[0], 'No virtual function "second" found in parent classes')
