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
		self.assertEqual(str(outContext), WppCore.strPack(expected))

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
		self.assertEqual(str(outContext), WppCore.strPack(expected))

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
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testCos(self):
		source = """
func public testCos: double
	param x: double
	Math.cos(x * 0.25)
		"""
		expected = """
import math

def testCos(x):
	return math.cos(x * 0.25)
		"""
		srcModule = WppCore.createMemModule(source, 'cos.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testPI(self):
		source = """var a : double = Math.PI * 0.75"""
		expected = """
import math

a = math.pi * 0.75
		"""
		srcModule = WppCore.createMemModule(source, 'pi.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
