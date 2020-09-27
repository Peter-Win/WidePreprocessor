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
"""
		module = TSCore.createModuleFromWpp(source, 'simpleOp.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
