import unittest
from Python.PyCore import PyCore
from Python.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyVar(unittest.TestCase):
	def testSimple(self):
		source = """
var const public myInt: int = 22
var const public myLong: long = -123456
var public myFloat: float = 1.23
var public myDouble: double = -1.23E+04
var myTrue: bool = true
var myFalse: bool = false
var defInt: int
var defULong: unsigned long
var defFloat: float
var defDouble: double
var defBool: bool
"""
		expected = """
myInt = 22
myLong = -123456
myFloat = 1.23
myDouble = -1.23E+04
myTrue = True
myFalse = False
defInt = 0
defULong = 0
defFloat = 0.0
defDouble = 0.0
defBool = False
"""
		module = PyCore.createModuleFromWpp(source, 'pyVar.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), expected.strip())