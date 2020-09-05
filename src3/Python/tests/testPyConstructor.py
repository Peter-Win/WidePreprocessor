import unittest
from Python.PyCore import PyCore
from Python.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyConstructor(unittest.TestCase):
	def testEmpty(self):
		source = """
class simple Point
	field public x: double = 0
var const pt: Point = Point()
var const x: double = pt.x
"""
		expect = """
class Point:
	__slots__ = ('x')
	def __init__(self):
		self.x = 0
pt = Point()
x = pt.x
"""
		module = PyCore.createModuleFromWpp(source, 'empty.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expect))

	def testSingle(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		param x0: double
		param y0: double
		x = x0
		y = y0
var const pt: Point = Point(22, 44)
var const x: double = pt.x
"""
		expect = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x0, y0):
		self.x = x0
		self.y = y0
pt = Point(22, 44)
x = pt.x
"""
		module = PyCore.createModuleFromWpp(source, 'empty.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expect))

	def testAutoinit(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x
		autoinit y
var const pt: Point = Point(22, 44)
var const x: double = pt.x
"""
		expect = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x, y):
		self.x = x
		self.y = y
pt = Point(22, 44)
x = pt.x
"""
		module = PyCore.createModuleFromWpp(source, 'autoinit.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expect))

	def testDefaultParams(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
var const pt0: Point = Point()
var const pt1: Point = Point(1)
var const pt2: Point = Point(1, 2)
"""
		expect = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
pt0 = Point()
pt1 = Point(1)
pt2 = Point(1, 2)
"""
		module = PyCore.createModuleFromWpp(source, 'defaultParams.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expect))

	def testOverload(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor overload
		x = 0
		y = 0
	constructor overload
		altName initPoint
		autoinit x
		autoinit y
	constructor overload
		altName copyPoint
		param src: const ref Point
		x = src.x
		y = src.y
var const first: Point = Point(1, 2)
var const second: Point = Point(first)
"""
		expected = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self):
		self.x = 0
		self.y = 0
	@staticmethod
	def initPoint(x, y):
		_inst = Point()
		_inst.x = x
		_inst.y = y
		return _inst
	@staticmethod
	def copyPoint(src):
		_inst = Point()
		_inst.x = src.x
		_inst.y = src.y
		return _inst
first = Point.initPoint(1, 2)
second = Point.copyPoint(first)
"""
		module = PyCore.createModuleFromWpp(source, 'overload.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
