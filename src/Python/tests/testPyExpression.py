import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyExpression(unittest.TestCase):
	def testConst(self):
		source = """
var public curYear: int = 2019
"""
		srcModule = WppCore.createMemModule(source, 'const.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
curYear = 2019
		"""
		self.assertEqual(str(outStream), expected.strip())

	def testBinOp(self):
		source = """
var first: double = 2.2
var public second: double = (first + 1.1) / 3.3
		"""
		srcModule = WppCore.createMemModule(source, 'binOp.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outStream = OutContextMemoryStream()
		dstModule.export(outStream)
		expected = """
__first = 2.2

second = (__first + 1.1) / 3.3
		"""
		self.assertEqual(str(outStream), expected.strip())
