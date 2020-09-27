import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon
from core.TaxonAltName import TaxonAltName

class TestWppOperator(unittest.TestCase):
	def testInvalidName(self):
		source = """
class simple One
	operator @: int
		param right: int
		return 1 + right
"""		
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'invalidName.wpp')
		self.assertEqual(cm.exception.args[0], 'Invalid operator name "@"')

	def testWrongOp(self):
		source = """
class simple One
	operator ?: int
		param right: int
		return 1 + right
"""		
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'WrongOp.wpp')
		self.assertEqual(cm.exception.args[0], 'Unable to override "?" operator')

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
var const b: Point = Point(0, -1)
var const c: Point = a + b
"""
		module = WppCore.createMemModule(source, 'simple.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testSimpleErr(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const *: Point
		param right: double
		return Point(x * right, y * right)

var const a: Point = Point(11, 22)
var const b: Point = Point(0, -1)
var const c: Point = a * b
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'simpleErr.wpp')
		self.assertEqual(cm.exception.args[0], 'Not found operator *(simple class Point, simple class Point)')
		self.assertEqual(cm.exception.args[1], ('simpleErr.wpp', 14, 'var const c: Point = a * b'))

	def testOverload(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const overload +: Point
		altName addNum
		param k: double
		return Point(x + k, y - k)
	operator const overload +: Point
		altName addPoint
		param pt: const ref Point
		return Point(x + pt.x, y + pt.y)
var const a: Point = Point(11, 22)
var const b: Point = a + 1.5
var const c: Point = a + b
"""
		module = WppCore.createMemModule(source, 'overload.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testOverloadErr(self):
		source = """
class simple One
	operator overload +: long
		param n: long
		return n + 1
	operator overload +: unsigned long
		param n: unsigned long
		return n + 1
var s: long = One() + 20
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'overloadErr.wpp')
		self.assertEqual(cm.exception.args[0], 'Multiple declarations for operator +(simple class One, int(20))')

	def testRight(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const right *: Point
		param left: double
		return Point(left * x, left * y)

var const a: Point = 1.23 * Point(11, 22)
"""
		module = WppCore.createMemModule(source, 'right.wpp')
		a = module.findItem('a')
		v = a.getValueTaxon()
		self.assertEqual(v.type, 'binop')
		decl = v.getDeclaration()
		self.assertEqual(decl.type, 'operator')
		self.assertEqual(decl.name, '*')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testRightOver(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const overload right *: Point
		altName rightMul
		param left: double
		return Point(left * x, left * y)
	operator const overload *: Point
		altName leftMul
		param right: double
		return Point(x * right, y * right)
var const a: Point = 1.23 * Point(11, 22)
var const b: Point = Point(1.1, 2.2) * 3.3
"""
		module = WppCore.createMemModule(source, 'right.wpp')

		a = module.findItem('a')
		decl = a.getValueTaxon().getDeclaration()
		self.assertEqual(TaxonAltName.getAltName(decl), 'rightMul')
		b = module.findItem('b')
		decl = b.getValueTaxon().getDeclaration()
		self.assertEqual(TaxonAltName.getAltName(decl), 'leftMul')

		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
