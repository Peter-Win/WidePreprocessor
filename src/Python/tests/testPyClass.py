if __name__=='__main__':
	import sys, os.path
	sys.path.append(os.path.abspath('../../'))

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
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

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
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

	def testMethodStatic(self):
		source = """
class public static MyMath
	method abs: double
		param value: double
		value < 0.0 ? -value : value

func public main
	var x: double = MyMath.abs(-3.14)
		"""
		expected = """
class MyMath:
	@staticmethod
	def abs(value):
		return -value if value < 0.0 else value

def main():
	x = MyMath.abs(-3.14)
		"""
		srcModule = WppCore.createMemModule(source, 'methodStatic.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		cls = dstModule.dictionary['MyMath']
		absOver = cls.dictionary['abs']
		absMethod = absOver.items[0]
		self.assertIn('static', absMethod.attrs)

		main = dstModule.dictionary['main'].items[0]
		cmd = main.getBody().items[0]
		self.assertEqual(cmd.type, 'Var')
		expr = cmd.getValueTaxon()
		self.assertEqual(expr.type, 'Call')
		pt = expr.getCaller()
		self.assertEqual(pt.getDebugStr(), '(MyMath . abs)')
		field = pt.getRight()
		self.assertEqual(field.type, 'FieldExpr')
		

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

	def testEmptyConstructor(self):
		srcModule = WppCore.createMemModule('class Con', 'con.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		classCon = dstModule.dictionary['Con']
		self.assertEqual(classCon.type, 'Class')
		con = classCon.createEmptyConstructor()
		self.assertEqual(con.type, 'Constructor')
		self.assertEqual(classCon.findConstructor(), con.owner)

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
		conOver = classTest.findConstructor()
		self.assertEqual(conOver.type, 'Overloads')
		con = conOver.items[0]
		self.assertEqual(con.type, 'Constructor')
		cmd2 = con.getBody().items[1]
		self.assertEqual(cmd2.type, 'BinOp')
		self.assertEqual(cmd2.opCode, '=')
		pt = cmd2.getLeft()
		self.assertEqual(pt.type, 'BinOp')
		self.assertEqual(pt.opCode, '.')
		field = pt.getRight()
		self.assertEqual(field.type, 'FieldExpr')
		self.assertEqual(field.id, 'second')

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
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

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
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

	def testSelfStatic(self):
		source = """
class Abc
	method static toa: String
		param s: String
		"[" + s + "]"
	method name: String
		toa("Hello")
		"""
		expected = """
class Abc:
	@staticmethod
	def toa(s):
		return '[' + s + ']'
	def name(self):
		return Abc.toa('Hello')
		"""
		srcModule = WppCore.createMemModule(source, 'staticFields.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))

	def testPyParamInit(self):
		source = """
class Point
	field public x: double
	field public y: double
	constructor
		param init x = 0
		param init y = 0
		"""
		expected = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		"""
		srcModule = WppCore.createMemModule(source, 'paramInit.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), WppCore.strPack(expected))
