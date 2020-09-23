import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPyBinOp(unittest.TestCase):
	def testArith(self):
		source = """
var const a: double = 1
var const b: double = 2
var const c: double = a + b * 3
var const d: double = (a + b) * c
var const e: double = a + (b * c)
"""
		expected = """
a = 1
b = 2
c = a + b * 3
d = (a + b) * c
e = a + b * c
"""		# В последней строке убираются ненужные скобки
		module = PyCore.createModuleFromWpp(source, 'arith.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testIntDiv(self):
		source = """
var const fres: double = 10.0 / 2.0
var const ires: int = 10 / 2
var const la: long = 10
var const lb: long = 2
var const lres: long = la / lb
var const ua: unsigned int = 10
var const ub: unsigned int = 2
var const ures: unsigned int = ua / ub
"""
		expected = """
fres = 10.0 / 2.0
ires = 10 // 2
la = 10
lb = 2
lres = la // lb
ua = 10
ub = 2
ures = ua // ub
"""
		module = PyCore.createModuleFromWpp(source, 'intDiv.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
		# module.core.printOps()

	def testLogic(self):
		source = """
var const a: int = 5
var const resAnd: bool = a > 0 && a < 10
var const resOr: bool = a < 0 || a > 10
"""
		expected = """
a = 5
resAnd = a > 0 and a < 10
resOr = a < 0 or a > 10
"""
		module = PyCore.createModuleFromWpp(source, 'logic.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testIntDivAssign(self):
		source = """
func test
	var a: int = 10
	a /= 2
"""
		expected = """
def test():
	a = 10
	a //= 2
"""
		module = PyCore.createModuleFromWpp(source, 'intDivAssign.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
