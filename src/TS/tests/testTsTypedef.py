import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsTypedef(unittest.TestCase):
	def testSimple(self):
		source = """
typedef TSize: unsigned long
		"""
		expected = 'export type TSize = number;'
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testInClass(self):
		source = """
class public Point
	typedef replace Value: double
	field public x: Value
class public Rect
	typedef replace Value: Point.Value
	field public x1: Value
		"""
		expected = """
export class Point {
	public x: number;
}
export class Rect {
	public x1: number;
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		Rect = dstModule.dictionary['Rect']
		Value = Rect.dictionary['Value']
		self.assertEqual(Value.type, 'Typedef')
		locType = Value.getTypeTaxon()
		self.assertEqual(locType.type, 'TypePath')

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testArrayReplace(self):
		source = """
class public A
	typedef replace Collection: Array String
class public B
	typedef Coll: A.Collection
	field public a: Coll
	method init
		param c: Coll
		a = c
		"""
		expected = """
export class A {
}
export class B {
	public a: string[];
	public init(c: string[]) {
		this.a = c;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testExtern(self):
		source = """
class public A
	typedef extern Collection: Array String
class public B
	typedef Coll: A.Collection
	field a: Coll
	method init
		param c: Coll
		a = c
		"""
		expected = """
export type ACollection = string[];
export class A {
}
export class B {
	private a: ACollection;
	public init(c: ACollection) {
		this.a = c;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'sextern.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testExternA(self):
		source = """
class public A
	typedef Collection: Array String
		altname AColl
class public B
	typedef Coll: A.Collection
	field public a: Coll
	method init
		param c: Coll
		a = c
		"""
		expected = """
export type AColl = string[];
export class A {
}
export class B {
	public a: AColl;
	public init(c: AColl) {
		this.a = c;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'sextern.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
