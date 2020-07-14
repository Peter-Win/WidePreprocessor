import unittest
from Wpp.WppFunc import WppFunc

class TestWppFunc(unittest.TestCase):
	def testParseHead(self):
		# full case
		errMsg, name, attrs, result = WppFunc.parseHead('func public overload myFunc: unsigned int')
		self.assertIsNone(errMsg)
		self.assertEqual(name, 'myFunc')
		self.assertEqual(attrs, {'public', 'overload'})
		self.assertEqual(result, 'unsigned int')

		# short case
		errMsg, name, attrs, result = WppFunc.parseHead('func print')
		self.assertIsNone(errMsg)
		self.assertEqual(name, 'print')
		self.assertEqual(attrs, set())
		self.assertIsNone(result)

		# error
		errMsg, name, attrs, result = WppFunc.parseHead('func')
		self.assertEqual(errMsg, 'Expected name of func')

		errMsg, name, attrs, result = WppFunc.parseHead('func: boolean')
		self.assertEqual(errMsg, 'Expected name of func')
