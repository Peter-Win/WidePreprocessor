import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyOperator(unittest.TestCase):
	def testMethod(self):
		source = """
class public Point
	field public x: double
	field public y: double
	operator +=: ref Point
		param pt: const ref Point
		x += pt.x
		y += pt.y
		this
		"""
		expected = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
	def __iadd__(self, pt):
		self.x += pt.x
		self.y += pt.y
		return self
		"""
		srcModule = WppCore.createMemModule(source, 'method.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testUnary(self):
		source = """
class public Point
	field public x: double
	field public y: double
	constructor
		param init x
		param init y

	operator const -: ref Point
		Point(-x, -y)
		"""
		expected = """
class Point:
	__slots__ = ('x', 'y')
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __neg__(self):
		return Point(-self.x, -self.y)
		"""
		srcModule = WppCore.createMemModule(source, 'method.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
