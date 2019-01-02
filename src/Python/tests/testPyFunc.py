import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyFunc(unittest.TestCase):
	def testFunc(self):
		source = """
func public lengthSqr: double
	param x: double
	param y: double
	x * x + y * y
"""
		expected = """
def lengthSqr(x, y):
	return x * x + y * y
		"""
		srcModule = WppCore.createMemModule(source, 'lengthSqr.fake')
		dstModule = srcModule.cloneRoot(PyCore())

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())