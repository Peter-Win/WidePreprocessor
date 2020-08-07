import unittest
from Wpp.WppFunc import WppFunc
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

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

	def testFunc(self):
		source = """
func public empty: double
	param x: double
	param y: double
	param z: double = 1
	var a: double = x
"""
		module = WppCore.createMemModule(source, 'func.wpp')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())

		func = module.findItem('empty')
		self.assertEqual(func.type, 'func')

		x = func.findParam('z')
		self.assertEqual(x.type, 'param')

		body = func.getBody()
		self.assertEqual(body.type, 'body')

		y = body.startFindUp('y')
		self.assertIsNotNone(y)
		self.assertEqual(y.type, 'param')
		self.assertEqual(y.name, 'y')

	def testDuplicateParams(self):
		source = """
func public abcd: double
	param abcd: int
	param abcd: double
	return abcd
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'dup.wpp')
		self.assertEqual(cm.exception.args[0], 'Duplicate identifier "abcd"')

	def testWrongDefaults(self):
		source = """
func public wrongDefault
	param first: int = 0
	param second: int
	param third: int = 0
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'defaultParam.wpp')
		self.assertEqual(cm.exception.args[0], 'Default parameters should be last.')


