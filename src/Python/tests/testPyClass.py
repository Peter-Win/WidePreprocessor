import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyClass(unittest.TestCase):
	def testParent(self):
		source = """
class public A
class public B
	# Class B
	extends A
		"""
		expected = """
class A:
	pass

class B(A):
	\"\"\" Class B \"\"\"
	pass
		"""
		srcModule = WppCore.createMemModule(source, 'ext.fake')
		pyCore = PyCore()
		dstModule = srcModule.clone(pyCore)
		dstModule.updateRefs()
		classA = dstModule.dictionary['A']
		classB = dstModule.dictionary['B']
		self.assertEqual(classB.type, 'Class')
		self.assertTrue(classB.canBeStatic)
		self.assertEqual(classB.name, 'B')
		self.assertEqual(classB.core, pyCore)
		self.assertEqual(classB.getParent(), classA)
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())

	def testMethod(self):
		source = """
class Norm
	method mul: double
		param coeff: double
		coeff * 10.0
		"""
		expected = """
class Norm:
	def mul(self, coeff):
		return coeff * 10.0
		"""
		srcModule = WppCore.createMemModule(source, 'method.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())

	def testMethodStatic(self):
		source = """
class static MyMath
	method abs: double
		param value: double
		value < 0.0 ? -value : value
func public main
	var x: double = MyMath.abs(-3.14)
		"""
		expected = """
class __MyMath:
	@staticmethod
	def abs(value):
		return -value if value < 0.0 else value

def main():
	x = __MyMath.abs(-3.14)
		"""
		srcModule = WppCore.createMemModule(source, 'methodStatic.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		cls = dstModule.dictionary['MyMath']
		absOver = cls.dictionary['abs']
		absMethod = absOver.items[0]
		self.assertIn('static', absMethod.attrs)

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())

	def testEmptyConstructor(self):
		srcModule = WppCore.createMemModule('class Con', 'con.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		classCon = dstModule.dictionary['Con']
		self.assertEqual(classCon.type, 'Class')
		con = classCon.createEmptyConstructor()
		self.assertEqual(con.type, 'Constructor')
		self.assertEqual(classCon.findConstructor(), con.owner)


	#@unittest.skip('Need getDefaultValue')
	def testFields(self):
		source = """
class public Parent
class public Test
	field public first: Parent
	field private second: Parent
	field public x: int = 1
	field public y: int
		"""
		srcModule = WppCore.createMemModule(source, 'fields.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		classTest = dstModule.dictionary['Test']
		first = classTest.dictionary['first']
		self.assertTrue(first.canBeStatic)

		expected = """
class Parent:
	pass

class Test:
	__slots__ = ('first', '__second', 'x', 'y')
	def __init__(self):
		self.first = None
		self.__second = None
		self.x = 1
		self.y = 0
		"""
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())

	def testStaticFields(self):
		source = """
class public A
class public B
	field static public ok: A
	field static hidden: A
		"""
		srcModule = WppCore.createMemModule(source, 'staticFields.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		expected = """
class A:
	pass

class B:
	ok = None
	__hidden = None
		"""
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())
