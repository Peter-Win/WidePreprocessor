import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyForeach(unittest.TestCase):
	def testSimple(self):
		source = """
func public main
	var myList: Array double = [0.1, 0.4, 0.8]
	var summa: double = 0.0
	foreach myList => var item
		summa += item
		"""
		expected = """
def main():
	myList = [0.1, 0.4, 0.8]
	summa = 0.0
	for item in myList:
		summa += item
		"""
		srcModule = WppCore.createMemModule(source, 'foreach.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testArrayIndex(self):
		source = """
func public main
	var myList: Array double = [0.1, 0.4, 0.8]
	var summa: double = 0.0
	foreach myList => var item => var i
		summa += item * (i + 1)
		"""
		expected = """
def main():
	myList = [0.1, 0.4, 0.8]
	summa = 0.0
	for i, item in enumerate(myList):
		summa += item * (i + 1)
		"""
		srcModule = WppCore.createMemModule(source, 'foreach.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())