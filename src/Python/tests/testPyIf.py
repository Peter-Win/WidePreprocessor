import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyIf(unittest.TestCase):

	def testSimple(self):
		source = """
func public positive: int
	param value: int
	if value < 0
		value = 0
	value
		"""
		expected = """
def positive(value):
	if value < 0:
		value = 0
	return value
		"""
		srcModule = WppCore.createMemModule(source, 'simpleIf.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())


	def testElse(self):
		source = """
func public getState: String
	param value: int
	var result: String
	if value < 0
		result = "Negative"
	else
		result = "Positive"
	result
		"""
		expected = """
def getState(value):
	result = ''
	if value < 0:
		result = 'Negative'
	else:
		result = 'Positive'
	return result
		"""
		srcModule = WppCore.createMemModule(source, 'elseIf.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext),  expected.strip())


	def testCases(self):
		source = """
func public getNumName: String
	param value: int
	var result: String
	if value == 0
		result = "Zero"
	elif value == 1
		result = "One"
	elif value == 2
		result = "Two"
	else
		result = "Else"
	result
		"""
		expected = """
def getNumName(value):
	result = ''
	if value == 0:
		result = 'Zero'
	elif value == 1:
		result = 'One'
	elif value == 2:
		result = 'Two'
	else:
		result = 'Else'
	return result
		"""
		srcModule = WppCore.createMemModule(source, 'elseIf.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())
