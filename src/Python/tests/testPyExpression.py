import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyExpression(unittest.TestCase):
	def testConst(self):
		source = """
var public curYear: int = 2019
"""
		srcModule = WppCore.createMemModule(source, 'const.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
curYear = 2019
		"""
		self.assertEqual(str(outStream), expected.strip())

	def testBinOp(self):
		source = """
var first: double = 2.2
var public second: double = (first + 1.1) / 3.3
		"""
		srcModule = WppCore.createMemModule(source, 'binOp.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
__first = 2.2

second = (__first + 1.1) / 3.3
		"""
		self.assertEqual(str(outStream), expected.strip())

	def testCall(self):
		source = """
func public func1: int
	param x: int
	x * 5
func public func2: int
	param a: int
	param b: int
	func1(a) + func1(b)
		"""
		srcModule = WppCore.createMemModule(source, 'binOp.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
def func1(x):
	return x * 5

def func2(a, b):
	return func1(a) + func1(b)
		"""
		self.assertEqual(str(outStream), expected.strip())

	def testSuper(self):
		source = """
class public A
	field public index: int
	constructor public
		param init index
class public B
	extends A
	field public mass: double
	constructor public
		param index: int
		param init mass
		super(index)
		"""
		srcModule = WppCore.createMemModule(source, 'binOp.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
class A:
	__slots__ = ('index')
	def __init__(self, index):
		self.index = index

class B(A):
	__slots__ = ('mass')
	def __init__(self, index, mass):
		super().__init__(index)
		self.mass = mass
		"""
		self.assertEqual(str(outStream), expected.strip())
