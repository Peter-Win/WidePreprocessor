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
