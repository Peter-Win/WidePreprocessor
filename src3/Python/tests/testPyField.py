import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPyField(unittest.TestCase):
	def testStatic(self):
		source = """
class public static Hello
	field static public first: int = 123
	field static private second: bool
"""
		expected = """
class Hello:
	first = 123
	second = False
"""
		module = PyCore.createModuleFromWpp(source, 'ststic.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))


	def testSimple(self):
		source = """
class public static Hello
	field public first: int = 123
	field private second: bool
"""
		expected = """
class Hello:
	__slots__ = ('first', 'second')
	def __init__(self):
		self.first = 123
		self.second = False
"""
		module = PyCore.createModuleFromWpp(source, 'simple.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))
	