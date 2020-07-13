import unittest
from Wpp.WppVar import WppCommonVar

class TestWppCommonVar(unittest.TestCase):

	def testParseMinimum(self):
		errMsg, name, attrs, typeDescr, valueDescr = WppCommonVar.parseHead('var count: int')
		self.assertEqual(errMsg, None)
		self.assertEqual(name, 'count')
		self.assertEqual(attrs, set())
		self.assertEqual(typeDescr, 'int')
		self.assertEqual(valueDescr, None)

	def testParseWithAttrsAndValue(self):
		errMsg, name, attrs, typeDescr, valueDescr = WppCommonVar.parseHead('field static public color: String = "black"')
		self.assertEqual(errMsg, None)
		self.assertEqual(name, 'color')
		self.assertEqual(attrs, set(['public', 'static']))
		self.assertEqual(typeDescr, 'String')
		self.assertEqual(valueDescr, '"black"')

	def testErrorNoType(self):
		""" Error situation. Expected ':' character """
		errMsg, name, attrs, typeDescr, value = WppCommonVar.parseHead('field static public color')
		self.assertEqual(errMsg, 'Expected ":" for type declaration')

	def testErrorNoName(self):
		""" Error situation. Name is not declared """
		errMsg, name, attrs, typeDescr, value = WppCommonVar.parseHead('var : int')
		self.assertEqual(errMsg, 'Expected name of var')
