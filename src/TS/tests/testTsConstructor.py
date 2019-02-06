import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

@unittest.skip('')
class TestTsConstructor(unittest.TestCase):
	def testOverloads(self):
		self.maxDiff = None
		source = """
class Point
	field public x: double
	field public y: double
	constructor
		param init x
		param init y
class public Rect
	field public A: Point
	field public B: Point
	constructor
		altname fromNums
		param x1: double
		param y1: double
		param x2: double
		param y2: double
		A = Point(x1, y1)
		B = Point(x2, y2)
	constructor
		altname fromPoints
		param init A
		param init B
func public main
	var const r1: Rect = Rect(10, 10, 60, 40)
	var const r2: Rect = Rect(Point(10, 10), Point(60, 40))
		"""
		expected = ''
		srcModule = WppCore.createMemModule(source, 'over.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

