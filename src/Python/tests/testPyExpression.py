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

	def testField(self):
		source = """
class public Field
	field public abcd: int
	method public copy
		param source: Field
		abcd = source.abcd
		"""
		expected = """
class Field:
	__slots__ = ('abcd')
	def __init__(self):
		self.abcd = 0
	def copy(self, source):
		self.abcd = source.abcd
		"""
		srcModule = WppCore.createMemModule(source, 'field.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		cls = dstModule.dictionary['Field']
		over = cls.dictionary['copy']
		method = over.items[0]
		eq = method.getBody().items[0]
		self.assertEqual(eq.type, 'BinOp')
		self.assertEqual(eq.getLeft().type, 'IdExpr')
		r = eq.getRight()
		self.assertEqual(r.type, 'BinOp')
		self.assertEqual(r.opCode, '.')
		self.assertEqual(r.getLeft().type, 'IdExpr')
		self.assertEqual(r.getLeft().id, 'source')
		f = r.getRight()
		self.assertEqual(f.id, 'abcd')
		self.assertEqual(f.type, 'FieldExpr')

		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
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

	def testNew(self):
		source = """
class public Uno
func public createUno: Uno
	Uno()
		"""
		expected = """
class Uno:
	pass

def createUno():
	return Uno()
		"""
		srcModule = WppCore.createMemModule(source, 'new.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
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

	def testTernary(self):
		source = """
func public isGood: int
	param value: double
	value < 1.0 ? 0 : 1
		"""
		expected = """
def isGood(value):
	return 0 if value < 1.0 else 1
		"""
		srcModule = WppCore.createMemModule(source, 'ternary.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		self.assertEqual(str(outStream), expected.strip())

	#@unittest.skip('Need fields')
	def testUnary(self):
		source = """
class public Unary
	field public first: int
	field public second: int
	method public init
		param value: int
		first = -value * -10
		second = -first
	method public cloneNeg
		param src: Unary
		first = -src.first + 1
		second = -(src.second + 1)
		"""
		expected0 = ''
		expected = """
class Unary:
	__slots__ = ('first', 'second')
	def __init__(self):
		self.first = 0
		self.second = 0
	def init(self, value):
		self.first = -value * -10
		self.second = -self.first
	def cloneNeg(self, src):
		self.first = -src.first + 1
		self.second = -(src.second + 1)
		"""
		srcModule = WppCore.createMemModule(source, 'unary.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		self.assertEqual(str(outStream), expected.strip())


	def testTranslation(self):
		source = """
func public And: bool
	param a: bool
	param b: bool
	a && b
		"""
		expected = """
def And(a, b):
	return a and b
		"""
		srcModule = WppCore.createMemModule(source, 'unary.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		self.assertEqual(str(outStream), expected.strip())
