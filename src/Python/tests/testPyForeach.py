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

	def testMapFull(self):
		""" Test for construction: for key, value in map.items() """
		source = """
func public toList: Array String
	param map: const Map String, String
	var result: Array String
	foreach map => var value => var key
		result.push(key + ":" + value)
	result
		"""
		expected = """
def toList(map):
	result = []
	for key, value in map.items():
		result.append(key + ':' + value)
	return result
		"""
		srcModule = WppCore.createMemModule(source, 'foreach.fake')
		dstModule = srcModule.cloneRoot(PyCore())

		toListOver = dstModule.dictionary['toList']
		self.assertEqual(toListOver.type, 'Overloads')
		toList = toListOver.items[0]
		self.assertEqual(toList.type, 'Func')
		cmdFor = toList.getBody().items[1]
		self.assertEqual(cmdFor.type, 'Foreach')
		cmdCall = cmdFor.getBody().items[0]
		self.assertEqual(cmdCall.type, 'Call')
		caller = cmdCall.getCaller()
		self.assertEqual(caller.type, 'BinOp')
		push = caller.getRight()
		self.assertEqual(push.type, 'FieldExpr')

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testMapValues(self):
		""" Test for construction: for value in map.values() """
		source = """
func public sumValues: double
	param map: const Map String, double
	var result: double = 0.0
	foreach map => var value
		result += value
	result
		"""
		expected = """
def sumValues(map):
	result = 0.0
	for value in map.values():
		result += value
	return result
		"""
		srcModule = WppCore.createMemModule(source, 'values.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
