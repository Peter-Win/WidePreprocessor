import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyMath(unittest.TestCase):
	def testAbs(self):
		source = """
func public testAbs: double
	param x: double
	Math.abs(x - 10)
		"""
		expected = """
def testAbs(x):
	return abs(x - 10)
		"""
		srcModule = WppCore.createMemModule(source, 'abs.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testSqrt(self):
		source = """
func public testSqrt: double
	param x: double
	Math.sqrt(x + 1)
		"""
		expected = """
def testSqrt(x):
	return sqrt(x + 1)
		"""
		srcModule = WppCore.createMemModule(source, 'sqrt.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testSqr(self):
		source = """
func public testSqr: double
	param x: double
	Math.sqr(x + 22)
		"""
		expected = """
def testSqr(x):
	return (x + 22) ** 2
		"""
		srcModule = WppCore.createMemModule(source, 'sqr.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testCos(self):
		source = """
func public testCos: double
	param x: double
	Math.cos(x * 0.25)
		"""
		expected = ''
		expected1 = """
import math
def testCos(x):
	return math.cos(x * 0.25)
		"""
		srcModule = WppCore.createMemModule(source, 'cos.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
