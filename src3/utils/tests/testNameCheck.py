import unittest
from utils.nameCheck import isUpperCamelCase, isLowerCamelCase

class TestNameCheck(unittest.TestCase):
	def testUpperCamelCase(self):
		self.assertTrue(isUpperCamelCase('A'))
		self.assertTrue(isUpperCamelCase('Abc'))
		self.assertTrue(isUpperCamelCase('ABC'))
		self.assertTrue(isUpperCamelCase('HelloWorld1'))

		self.assertFalse(isUpperCamelCase(''))
		self.assertFalse(isUpperCamelCase('abc'))
		self.assertFalse(isUpperCamelCase('_Abcd'))
		self.assertFalse(isUpperCamelCase('HELLO_WORLD'))
		self.assertFalse(isUpperCamelCase('HelloWorld!'))

	def testLowerCamelCase(self):
		self.assertTrue(isLowerCamelCase('a'))
		self.assertTrue(isLowerCamelCase('abc'))
		self.assertTrue(isLowerCamelCase('abcXyz'))
		self.assertTrue(isLowerCamelCase('lowerCamelCase123'))

		self.assertFalse(isLowerCamelCase(''))
		self.assertFalse(isLowerCamelCase('Abc'))
		self.assertFalse(isLowerCamelCase('_abcd'))
		self.assertFalse(isLowerCamelCase('hello_world'))
		self.assertFalse(isLowerCamelCase('lowerCamelCase!'))