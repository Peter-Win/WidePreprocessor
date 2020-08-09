import unittest
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream
from Python.style import style

class TestPyMethod(unittest.TestCase):

	def testSimple(self):
		source = """
class public static Hello
	method getCount: unsigned int
		return 1234
	method setCount
		param count: unsigned int
		param bUpdate: bool = false
"""
		expected = """
class Hello:
	def getCount(self):
		return 1234
	def setCount(self, count, bUpdate = False):
		pass
"""
		module = PyCore.createModuleFromWpp(source, 'simple.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))


	def testStatic(self):
		source = """
class public static Hello
	method static getCount: unsigned int
		return 1234
	method static setCount
		param count: unsigned int
		param bUpdate: bool = false
"""
		expected = """
class Hello:
	@staticmethod
	def getCount():
		return 1234
	@staticmethod
	def setCount(count, bUpdate = False):
		pass
"""
		module = PyCore.createModuleFromWpp(source, 'static.wpp')
		out = OutContextMemoryStream()
		module.exportContext(out, style)
		self.assertEqual(str(out), PyCore.strPack(expected))
