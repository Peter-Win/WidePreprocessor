import unittest
from Wpp.WppFunc import WppFunc
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

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

