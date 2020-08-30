import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppConstructor(unittest.TestCase):
	def testSimple(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		param x0: double
		param y0: double
		x = x0
		y = y0
var pt: Point = Point(1.11, 2.22)
var x: double = pt.x
"""
		module = WppCore.createMemModule(source, 'simple.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testAutoinit(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x
		autoinit y
var pt: Point = Point(1.11, 2.22)
"""
		module = WppCore.createMemModule(source, 'autoinit.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
		p = module.findItem('Point')
		con = p.findConstructor()
		x = con.findItem('x')
		self.assertEqual(x.getTypeTaxon().exportString(), 'double')
		self.assertEqual(x.buildQuasiType().getDebugStr(), 'double')

	def testOverload(self):
		source = """
class simple Point
	field x: double
	field y: double
	constructor overload
		autoinit x
		autoinit y
	constructor overload
		param pt: const ref Point
		x = pt.x
		y = pt.y
var const a: Point = Point(33, 44)
var const b: Point = Point(a)
"""
		module = WppCore.createMemModule(source, 'overload.wpp')
		Point = module.findItem('Point')
		self.assertEqual(Point.type, 'class')
		con = Point.findConstructor()
		self.assertEqual(con.type, 'overload')

		a = module.findItem('a')
		newA = a.getValueTaxon()
		self.assertEqual(newA.type, 'new')
		self.assertEqual(newA.overloadIndex, 0)

		b = module.findItem('b')
		self.assertEqual(b.getValueTaxon().overloadIndex, 1)

		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
