import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPyOperator(unittest.TestCase):
	def testSimple(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const +: Point
		param right: const ref Point
		return Point(x + right.x, y + right.y)

var const a: Point = Point(11, 22)
var const b: Point = a + Point(0, -1)
"""
		expected = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
	def __add__(self, right):
		return Point(self.x + right.x, self.y + right.y)
a = Point(11, 22)
b = a + Point(0, -1)
"""
		module = PyCore.createModuleFromWpp(source, 'simple.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testRight(self):
		source = """
class simple Value
	field value: int
	constructor
		autoinit value
	operator const right /: Value
		param divident: int
		return Value(divident / value)
var const v: Value = 1000 / Value(22)
"""
		expected = """
class Value:
	__slots__ = ('value')
	def __init__(self, value):
		self.value = value
	def __rtruediv__(self, divident):
		return Value(divident // self.value)
v = 1000 / Value(22)
"""
		module = PyCore.createModuleFromWpp(source, 'right.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testOverload(self):
		source = """
class simple Point
	field x: double
	field y: double
	constructor
		autoinit x
		autoinit y
	operator const overload +: Point
		param p: Point
		return Point(x + p.x, y + p.y)
	operator const overload +: Point
		param k: double
		return Point(x + k, y + k)
	method const overload plus: Point
		altName plusPt
		param p: const ref Point
		return Point(x + p.x, y + p.y)
	method const overload plus: Point
		altName plusN
		param k: double
		return Point(x + k, y + k)
var const a: Point = Point(11, 22) + 3
var const b: Point = a + Point(-1, -2)
var const a1: Point = Point(11, 22).plus(3)
var const b1: Point = a1.plus(Point(-1, -2))
"""
		expected = """
"""
		module = PyCore.createModuleFromWpp(source, 'overload.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
