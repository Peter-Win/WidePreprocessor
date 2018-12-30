import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyClass(unittest.TestCase):
	def testParent(self):
		source = """
class public A
class public B
	extends A
		"""
		expected = """
class A:
	pass

class B(A):
	pass
		"""
		srcModule = WppCore.createMemModule(source, 'ext.fake')
		dstModule = srcModule.clone(PyCore())
		dstModule.updateRefs()
		classA = dstModule.dictionary['A']
		classB = dstModule.dictionary['B']
		self.assertEqual(classB.type, 'Class')
		self.assertEqual(classB.name, 'B')
		self.assertEqual(classB.getParent(), classA)
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), expected.strip())
