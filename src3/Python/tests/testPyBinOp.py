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