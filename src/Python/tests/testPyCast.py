import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyCast(unittest.TestCase):
	def testString(self):
		source = """
class A
	field public s: String
	cast const: String
		s 
		"""
		expected = """
class A:
	__slots__ = ('s')
	def __init__(self):
		self.s = ''
	def __str__(self):
		return self.s
		"""
		srcModule = WppCore.createMemModule(source, 'A.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())