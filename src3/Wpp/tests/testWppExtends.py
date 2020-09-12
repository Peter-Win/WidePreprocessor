import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon
from core.QuasiType import QuasiType

class TestWppExtends(unittest.TestCase):
	def testSimple(self):
		source = """
class A
class B
	extends A
"""
		module = WppCore.createMemModule(source, 'simple.wpp')

		A = module.findItem('A')
		self.assertIsNone(A.getExtends())
		B = module.findItem('B')
		ext = B.getExtends()
		self.assertEqual(ext.getParent(), A)

		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testDoubleError(self):
		source = """
class A
class B
class C
	extends A
	extends B
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'doubleErr.wpp')
		self.assertEqual(cm.exception.args[0], 'Only one parent class is allowed.')

	def testFindParentByName(self):
		source = """
class Top
class Middle
	extends Top
class Bottom
	extends Middle
"""
		module = WppCore.createMemModule(source, 'findParentByName.wpp')
		Top = module.findItem('Top')
		Middle = module.findItem('Middle')
		Bottom = module.findItem('Bottom')
		self.assertIsNone(Top.getParent())
		self.assertEqual(Middle.getParent(), Top)
		self.assertEqual(Bottom.getParent(), Middle)
		self.assertEqual(Bottom.findParentByName('Top'), Top)
		self.assertEqual(Bottom.findParentByName('Middle'), Middle)
		self.assertIsNone(Bottom.findParentByName('Abcd'))
		self.assertEqual(QuasiType.matchTaxons(Top, Middle), ('upcast', None))
		self.assertEqual(QuasiType.matchTaxons(Top, Bottom), ('upcast', None))
		self.assertEqual(QuasiType.matchTaxons(Top, Top), ('exact', None))

	def testUpcast(self):
		source = """
class Parent
class Child
	extends Parent
var const a: Child = Child()
var const b: Parent = a
var const c: Parent = Child()
"""
		module = WppCore.createMemModule(source, 'upcast.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testCastError(self):
		source = """
class Parent
class Child
	extends Parent
var const b: Parent = Child()
var const c: Child = b
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'castErr.wpp')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "class Parent" to "Child"')
		self.assertEqual(cm.exception.args[1], ('castErr.wpp', 6, 'var const c: Child = b'))

	def testMemberAccess(self):
		source = """
class Parent
	field public primary: double = 1
class Child
	extends Parent
	field public secondary: double = 2
var const child: Child = Child()
var const secondary: double = child.secondary
var const primary: double = child.primary
"""
		module = WppCore.createMemModule(source, 'memberAccess.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testMemberAccessInternal(self):
		source = """
class Parent
	field public primary: double = 1
class Child
	extends Parent
	method const getPrimary: double
		return primary
"""
		module = WppCore.createMemModule(source, 'memberAccessInternal.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
