import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsOperator(unittest.TestCase):
	def testBase(self):
		source = """
class Point
	field x: double
	field y: double

	constructor
		param init x
		param init y

	operator +=: ref Point
		param pt: const ref Point
		x += pt.x
		y += pt.y
		this

	operator const +: Point
		param pt: const ref Point
		Point(x + pt.x, y + pt.y)

	operator const right *: Point
		param k: double
		Point(k * x, k * y)

	operator const -: Point
		Point(-x, -y)
		"""
		expected = """
export class Point {
	private x: number;
	private y: number;
	public constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}
	public iadd(pt: Point): Point {
		this.x += pt.x;
		this.y += pt.y;
		return this;
	}
	public add(pt: Point): Point {
		return new Point(this.x + pt.x, this.y + pt.y);
	}
	public rmul(k: number): Point {
		return new Point(k * this.x, k * this.y);
	}
	public neg(): Point {
		return new Point(-this.x, -this.y);
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testMinus(self):
		source = """
class Point
	field x: double
	field y: double
	constructor
		param init x
		param init y
	operator -: Point
		param pt: Point
		Point(x - pt.x, y - pt.y)
	operator -: Point
		Point(-x, -y)
		"""
		expected = """
export class Point {
	private x: number;
	private y: number;
	public constructor(x: number, y: number) {
		this.x = x;
		this.y = y;
	}
	public sub(pt: Point): Point {
		return new Point(this.x - pt.x, this.y - pt.y);
	}
	public neg(): Point {
		return new Point(-this.x, -this.y);
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'minus.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		classPoint = dstModule.dictionary['Point']
		minusOver = classPoint.dictionary['-']
		self.assertEqual(minusOver.type, 'Overloads')
		self.assertEqual(len(minusOver.items), 2)

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
