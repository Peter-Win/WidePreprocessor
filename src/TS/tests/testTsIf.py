import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsIf(unittest.TestCase):
	def testSimple(self):
		source = """
func public testValue: String
	param value: double
	if value < 0
		return "Negative"
	"Positive"
		"""
		expected = """
export function testValue(value: number): string {
	if (value < 0) {
		return 'Negative';
	}
	return 'Positive';
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testElse(self):
		source = """
func public testValue: String
	param value: double
	var result: String
	if value < 0
		result = "Negative"
	else
		result = "Positive"
	result
		"""
		expected = """
export function testValue(value: number): string {
	let result: string;
	if (value < 0) {
		result = 'Negative';
	} else {
		result = 'Positive';
	}
	return result;
}
		"""
		srcModule = WppCore.createMemModule(source, 'else.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())

	def testComplex(self):
		source = """
func public testValue: String
	param value: int
	var result: String
	if value == 0
		result = "Zero"
	elif value == 1
		result = "One"
	elif value == 2
		result = "Two"
	else
		result = String(value)
	result
		"""
		expected = """
export function testValue(value: number): string {
	let result: string;
	if (value === 0) {
		result = 'Zero';
	} else if (value === 1) {
		result = 'One';
	} else if (value === 2) {
		result = 'Two';
	} else {
		result = String(value);
	}
	return result;
}
		"""
		srcModule = WppCore.createMemModule(source, 'else.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())