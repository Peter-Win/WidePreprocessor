import unittest
from TS.TSCore import TSCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.style import style

class TestTSBinOp(unittest.TestCase):
	def testArith(self):
		source = """
var const a: double = 1
var const b: double = 2
var const c: double = a + b * 3
var const d: double = (a + b) * c
var const e: double = a + (b * c)
"""
		expected = """
const a = 1;
const b = 2;
const c = a + b * 3;
const d = (a + b) * c;
const e = a + b * c;
"""		# В последней строке убираются ненужные скобки
		module = TSCore.createModuleFromWpp(source, 'arith.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))