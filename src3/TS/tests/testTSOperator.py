import unittest
from TS.TSCore import TSCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.style import style

class TestTSOperator(unittest.TestCase):
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
class Point {
    public x: number;
    public y: number;
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    add(right: Point): Point {
        return new Point(this.x + right.x, this.y + right.y);
    }
}
const a = new Point(11, 22);
const b = a.add(new Point(0, -1));
"""
		module = TSCore.createModuleFromWpp(source, 'simpleOp.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testRightSimple(self):
		source = """
class simple Point
	field x: double
	field y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const right *: Point
		param k: double
		return Point(k * x, k * y)
var const p: Point = 10 * Point(1, 2)
"""
		expected = """
class Point {
    private x: number;
    private y: number;
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    rmul(k: number): Point {
        return new Point(k * this.x, k * this.y);
    }
}
const p = new Point(1, 2).rmul(10);
"""
		module = TSCore.createModuleFromWpp(source, 'simpleRight.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testOverload(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const overload +: Point
		altName addPoint
		param right: const ref Point
		return Point(x + right.x, y + right.y)
	operator const overload +: Point
		altName addNum
		param n: double
		return Point(x + n, y + n)

var const a: Point = Point(11, 22) + 33
var const b: Point = a + Point(0, -1)
"""
		expected = """
class Point {
    public x: number;
    public y: number;
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    addPoint(right: Point): Point {
        return new Point(this.x + right.x, this.y + right.y);
    }
    addNum(n: number): Point {
        return new Point(this.x + n, this.y + n);
    }
}
const a = new Point(11, 22).addNum(33);
const b = a.addPoint(new Point(0, -1));
"""
		module = TSCore.createModuleFromWpp(source, 'overload.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testOverloadRight(self):
		source = """
class simple Point
	field public x: double
	field public y: double
	constructor
		autoinit x = 0
		autoinit y = 0
	operator const overload *: Point
		param right: double
		return Point(x * right, y * right)
	operator const overload right *: Point
		param left: double
		return Point(left * x, left * y)

var const a: Point = Point(11, 22) * 33
var const b: Point = 1.1 * Point(0, -1)
"""
		expected = """
class Point {
    public x: number;
    public y: number;
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    mul(right: number): Point {
        return new Point(this.x * right, this.y * right);
    }
    rmul(left: number): Point {
        return new Point(left * this.x, left * this.y);
    }
}
const a = new Point(11, 22).mul(33);
const b = new Point(0, -1).rmul(1.1);
"""
		module = TSCore.createModuleFromWpp(source, 'overloadR.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))


