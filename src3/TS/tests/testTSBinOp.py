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

	def testIntDiv(self):
		source = """
var const sA: int = 10
var const sB: int = 3
var const s1: int = sA / sB
var const s2: int = sA / sB + 1
var const s3: int = sA / 3
var const s4: int = 1000 / sB
"""
		expected = """
const sA = 10;
const sB = 3;
const s1 = sA / sB | 0;
const s2 = (sA / sB | 0) + 1;
const s3 = sA / 3 | 0;
const s4 = 1000 / sB | 0;
"""
		# sA / sB  => sA / sB | 0   Необходимо использовать | 0, т.к. результат должен быть целым числом 10 // 3 = 3
		# sA / sB + 1 => (sA / sB | 0) + 1  Применяются скобки, т.к. приоритет операции | ниже, чем +
		module = TSCore.createModuleFromWpp(source, 'intDiv.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
