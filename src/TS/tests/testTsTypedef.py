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
	typedef Value: double
class public Rect
	typedef Value: Point.Value
		"""
		expected = """
export class Point {
	public type Value = number;
}
export class Rect {
	public type Value = Point.Value;
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
