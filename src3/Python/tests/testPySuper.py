import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPySuper(unittest.TestCase):
	def testConstructor(self):
		source = """
class First
	field primary: int
	constructor
		autoinit primary
class Second
	extends First
	field secondary: double
	constructor
		param primary: int
		autoinit secondary
		super(primary)
"""
		expected = """
class First:
	__slots__ = ('primary')
	def __init__(self, primary):
		self.primary = primary
class Second(First):
	__slots__ = ('secondary')
	def __init__(self, primary, secondary):
		super().__init__(primary)
		self.secondary = secondary
"""
		module = PyCore.createModuleFromWpp(source, 'superInCon.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))

	def testOverride(self):
		source = """
class First
	method virtual getValue: int
		param id: int
		return id * 2
class Second
	extends First
	method override getValue: int
		param id: int
		return super(id) + 1
"""
		expected = """
class First:
	def getValue(self, id):
		return id * 2
class Second(First):
	def getValue(self, id):
		return super().getValue(id) + 1
"""
		module = PyCore.createModuleFromWpp(source, 'superInOver.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))
