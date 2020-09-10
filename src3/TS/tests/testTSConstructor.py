import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSConstructor(unittest.TestCase):
	def testEmpty(self):
		source = """
class simple Point
	field public x: double = 0
var const pt: Point = Point()
var const x: double = pt.x
"""
		expect = """
class Point {
    public x = 0;
}
const pt = new Point();
const x = pt.x;
"""
		module = TSCore.createModuleFromWpp(source, 'empty.wpp')
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
class Point {
    public x: number;
    public y: number;
    constructor(x0: number, y0: number) {
        this.x = x0;
        this.y = y0;
    }
}
const pt = new Point(22, 44);
const x = pt.x;
"""
		module = TSCore.createModuleFromWpp(source, 'single.wpp')
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
class Point {
    public x: number;
    public y: number;
    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
}
const pt = new Point(22, 44);
const x = pt.x;
"""
		module = TSCore.createModuleFromWpp(source, 'autoinit.wpp')
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
class Point {
    public x: number;
    public y: number;
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
}
const pt0 = new Point();
const pt1 = new Point(1);
const pt2 = new Point(1, 2);
"""
		module = TSCore.createModuleFromWpp(source, 'defaultParams.wpp')
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
var const org: Point = Point()
var const first: Point = Point(1, 2)
var const second: Point = Point(first)
"""
		expected = """
class Point {
    public x: number;
    public y: number;
    constructor() {
        this.x = 0;
        this.y = 0;
    }
    static initPoint(x: number, y: number): Point {
        const _inst = new Point();
        _inst.x = x;
        _inst.y = y;
        return _inst;
    }
    static copyPoint(src: Point): Point {
        const _inst = new Point();
        _inst.x = src.x;
        _inst.y = src.y;
        return _inst;
    }
}
const org = new Point();
const first = Point.initPoint(1, 2);
const second = Point.copyPoint(first);
"""
		module = TSCore.createModuleFromWpp(source, 'overload.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
