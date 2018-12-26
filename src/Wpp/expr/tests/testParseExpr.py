import unittest
from Wpp.expr.parseExpr import parseExpr
from Wpp.Context import Context
from core.ErrorTaxon import ErrorTaxon

class TestParseExpr(unittest.TestCase):
	def testConst(self):
		ctx = Context.createFromMemory('', 'fake')

		res1 = parseExpr('123', ctx)
		self.assertEqual(len(res1), 2)
		self.assertEqual(res1[0], ('123', 'const', 'int'))
		self.assertEqual(res1[1], ('end', 'cmd', None))

		res2 = parseExpr('12.3', ctx)
		self.assertEqual(len(res2), 2)
		self.assertEqual(res2[0], ('12.3', 'const', 'fixed'))

		res3 = parseExpr('1.23E+06', ctx)
		self.assertEqual(len(res3), 2)
		self.assertEqual(res3[0], ('1.23E+06', 'const', 'float'))

		res4 = parseExpr('1.23E-06', ctx)
		self.assertEqual(len(res4), 2)
		self.assertEqual(res4[0], ('1.23E-06', 'const', 'float'))

		res5 = parseExpr('-1', ctx)
		self.assertEqual(len(res5), 3)
		self.assertEqual(res5[0], ('-', 'cmd', None))
		self.assertEqual(res5[1], ('1', 'const', 'int'))

	def testStrings(self):
		ctx = Context.createFromMemory('', 'fake')
		res = parseExpr('"Abcd"', ctx)
		self.assertEqual(len(res), 2)
		self.assertEqual(res[0], ('Abcd', 'const', 'string'))
		self.assertEqual(res[1], ('end', 'cmd', None))

		res = parseExpr('"First\\nSecond"', ctx)
		self.assertEqual(len(res), 2)
		self.assertEqual(res[0], ('First\nSecond', 'const', 'string'))

		res = parseExpr('"\\t\\\\"', ctx)
		self.assertEqual(len(res), 2)
		self.assertEqual(res[0], ('\t\\', 'const', 'string'))

		res = parseExpr('"D\\\'Artagnan"', ctx)
		self.assertEqual(len(res), 2)
		self.assertEqual(res[0], ('D\'Artagnan', 'const', 'string'))

		res = parseExpr('"Say: \\"Hello!\\""', ctx)
		self.assertEqual(len(res), 2)
		self.assertEqual(res[0], ('Say: "Hello!"', 'const', 'string'))

		# Invalid cases
		with self.assertRaises(ErrorTaxon) as ex:
			res = parseExpr('"Hello', ctx)
		self.assertEqual(ex.exception.args[0], 'String is not closed')
		with self.assertRaises(ErrorTaxon) as ex:
			res = parseExpr('"abc\\"', ctx)
		self.assertEqual(ex.exception.args[0], 'String is not closed')
		with self.assertRaises(ErrorTaxon) as ex:
			res = parseExpr('"\\Z"', ctx)
		self.assertEqual(ex.exception.args[0], 'Invalid escape char: Z')

	def testIds(self):
		ctx = Context.createFromMemory('', 'fake')
		res = parseExpr('A Abc Size640x480', ctx)
		self.assertEqual(len(res), 4)
		self.assertEqual(res[0], ('A', 'id', None))
		self.assertEqual(res[1], ('Abc', 'id', None))
		self.assertEqual(res[2], ('Size640x480', 'id', None))

	def testMinus(self):
		ctx = Context.createFromMemory('', 'fake')
		res = parseExpr('A-1', ctx)
		self.assertEqual(len(res), 4)
		self.assertEqual(res[0], ('A', 'id', None))
		self.assertEqual(res[1], ('-', 'cmd', None))
		self.assertEqual(res[2], ('1', 'const', 'int'))

	def testCommands(self):
		ctx = Context.createFromMemory('', 'fake')
		res = parseExpr('( && )\t*[/] <=', ctx)
		self.assertEqual(len(res), 9)
		self.assertEqual(res[0], ('(', 'cmd', None))
		self.assertEqual(res[1], ('&&', 'cmd', None))
		self.assertEqual(res[2], (')', 'cmd', None))
		self.assertEqual(res[3], ('*', 'cmd', None))
		self.assertEqual(res[4], ('[', 'cmd', None))
		self.assertEqual(res[5], ('/', 'cmd', None))
		self.assertEqual(res[6], (']', 'cmd', None))
		self.assertEqual(res[7], ('<=', 'cmd', None))

	def testWrongExpressions(self):
		ctx = Context.createFromMemory('', 'fake')
		with self.assertRaises(ErrorTaxon) as ex:
			res = parseExpr('_hello', ctx)	# Wrong character _
		self.assertEqual(ex.exception.args[0], 'Invalid character "_" in expression _hello')