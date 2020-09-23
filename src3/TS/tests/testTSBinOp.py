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

	def testCmp(self):
		source = """
var const a: int = 5
var const eq: bool = a == 0
var const ne: bool = a != 0 
"""
		expected = """
const a = 5;
const eq = a === 0;
const ne = a !== 0;
"""
		module = TSCore.createModuleFromWpp(source, 'cmp.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testShift(self):
		source = """
var const s: int = 128
var const u: unsigned int = 128
var const sl: int = s << 2
var const ul: unsigned int = u << 2
var const sr: int = s >> 2
var const ur: unsigned int = u >> 2
"""
		expected = """
const s = 128;
const u = 128;
const sl = s << 2;
const ul = u << 2;
const sr = s >> 2;
const ur = u >>> 2;
"""
		module = TSCore.createModuleFromWpp(source, 'shift.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
