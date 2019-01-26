import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsClass(unittest.TestCase):
	def testSimple(self):
		source = """
class TsClassA

class public TsClassB
	# Comment
	extends TsClassA
		"""
		expected = """
class TsClassA {
}

// Comment
export class TsClassB extends TsClassA {
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testStatic(self):
		source = """
class static MyMath
	field public Pi: double = 3.1415926
	method abs: double
		param x: double
		x < 0 ? -x : x

func public main
	var const x: double = MyMath.abs(MyMath.Pi * 123)
		"""
		expected = """
class MyMath {
	public static Pi: number = 3.1415926;
	public static abs(x: number): number {
		return x < 0 ? -x : x;
	}
}
export function main() {
	const x: number = MyMath.abs(MyMath.Pi * 123);
}
		"""
		srcModule = WppCore.createMemModule(source, 'static.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testConstructor(self):
		source = """
class Point
	field x: double
	field y: double
	constructor
		param init x = 0
		param init y = 0
		"""
		expected = """
export class Point {
	private x: number;
	private y: number;
	public constructor(x: number = 0, y: number = 0) {
		this.x = x;
		this.y = y;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'static.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
