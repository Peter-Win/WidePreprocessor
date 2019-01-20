import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyTypedef(unittest.TestCase):
	def testClass(self):
		source = """
class public Point
	typedef Value: double
	field public x: Value
		"""
		expected = """
class Point:
	__slots__ = ('x')
	def __init__(self):
		self.x = 0.0
		"""
		srcModule = WppCore.createMemModule(source, 'typedef.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
