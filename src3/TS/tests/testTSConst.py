import unittest
from TS.TSExpression import TSConst
from Wpp.WppExpression import WppConst
from TS.TSCore import TSCore

singleStyle = {'singleQuote': True}
doubleStyle = {'singleQuote': False}
tsCore = TSCore.createInstance()

def fromWpp(stringValue):
	wpp = WppConst.create(stringValue)
	return wpp.clone(tsCore)

class TestTSConst(unittest.TestCase):
	def testString(self):
		self.assertEqual(TSConst.makeString('Hello', singleStyle), "'Hello'")
		self.assertEqual(TSConst.makeString('Hello', doubleStyle), '"Hello"')

		self.assertEqual(TSConst.makeString('\t"Hello"\r\n', singleStyle), """'\\t"Hello"\\r\\n'""")
		self.assertEqual(TSConst.makeString('\t"Hello"\r\n', doubleStyle), '''"\\t\\"Hello\\"\\r\\n"''')

	def testClone(self):
		wppInt = WppConst.create('123')
		self.assertEqual(wppInt.constType, 'int')
		self.assertEqual(wppInt.value, 123)
		tsInt = wppInt.clone(tsCore)
		self.assertEqual(tsInt.type, 'const')
		self.assertEqual(tsInt.constType, 'int')
		self.assertEqual(tsInt.value, 123)

		tsTrue = fromWpp('true')
		self.assertEqual(tsTrue.type, 'const')
		self.assertEqual(tsTrue.constType, 'bool')
		self.assertTrue(tsTrue.value)

	def testExportNull(self):
		txNull = fromWpp('null')
		lexems = []
		txNull.exportLexems(lexems, singleStyle)
		self.assertEqual(lexems, [('null', 'const')])

	def testExportBool(self):
		txTrue = fromWpp('true')
		self.assertEqual(txTrue.constType, 'bool')
		self.assertTrue(txTrue.value)
		txFalse = fromWpp('false')
		self.assertEqual(txFalse.constType, 'bool')
		self.assertFalse(txFalse.value)
		lexems = []
		txTrue.exportLexems(lexems, singleStyle)
		txFalse.exportLexems(lexems, singleStyle)
		self.assertEqual(lexems, [('true', 'const'), ('false', 'const')])

	def testExportNumber(self):
		taxons = [
			fromWpp('123'),
			fromWpp('-5'),
			fromWpp('3.14'),
			fromWpp('1.11E+3'),
			fromWpp('1.23E-6'),
		]
		values = [tx.value for tx in taxons]
		self.assertEqual(values, [123, -5, 3.14, 1.11E+3, 1.23E-6])
		lexems = []
		for tx in taxons:
			tx.exportLexems(lexems, singleStyle)
		self.assertEqual(lexems, [
			('123', 'const'),
			('-5', 'const'),
			('3.14', 'const'),
			('1.11E+3', 'const'),
			('1.23E-6', 'const'),
		])

	def testExportString(self):
		txHello = TSConst('string', 'Hello')
		lexems = []
		txHello.exportLexems(lexems, singleStyle)
		self.assertEqual(lexems, [("'Hello'", 'const')])

