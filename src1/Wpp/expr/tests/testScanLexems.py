import unittest
from Wpp.expr.scanLexems import scanLexems
from Wpp.Context import Context
from core.ErrorTaxon import ErrorTaxon

class TestScanLexems(unittest.TestCase):
	def testArithmetic(self):
		ctx = Context.createFromMemory('', 'fake')
		# 2 + 3 * 5
		lexems = [('2', 'const', 'int'), ('+', 'cmd', None), ('3', 'const', 'int'), ('*', 'cmd', None), ('5', 'const', 'int'), ('end', 'cmd', None)]
		node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(node.type, 'binop')
		self.assertEqual(node.export(), '2 + 3 * 5')

		# (2 + 3) * 5
		lexems = [('(', 'cmd', None), ('2', 'const', 'int'), ('+', 'cmd', None), ('3', 'const', 'int'), (')', 'cmd', None),
		('*', 'cmd', None), ('5', 'const', 'int'), (',', 'cmd', None)]
		node, pos = scanLexems(lexems, 0, {','}, ctx)
		self.assertEqual(node.export(), '(2 + 3) * 5')

	def testMinusChange(self):
		ctx = Context.createFromMemory('', 'fake')
		lexems = [('-','cmd',None), ('3.14','const','float'), ('end','cmd',None)]
		node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(node.type, 'arg')
		self.assertEqual(node.value, '-3.14')

	def testTernaryOp(self):
		ctx = Context.createFromMemory('', 'fake')
		# a == -1 ? str(n + 42) : "Hello!"
		lexems = [('a','id',None), ('==','cmd',None), ('-','cmd',None), ('1','const','int'),
		('?','cmd',None), ('str','id',None), ('(','cmd',None), ('n','id',None), ('+','cmd',None),
		('42','const','int'), (')','cmd',None), (':','cmd',None), ('Hello!','const','string'), ('end','cmd',None)]
		node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(node.export(), 'a == -1 ? str(n + 42) : "Hello!"')

	def testArrayIndex(self):
		ctx = Context.createFromMemory('', 'fake')
		lexems = [('vector','id',None), ('[','cmd',None), ('N','id',None), ('-','cmd',None), ('1','const','int'), (']','cmd',None), ('end','cmd',None)]
		node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(node.type, 'index')
		self.assertEqual(node.export(), 'vector[N - 1]')


	def testInvalidLexems(self):
		ctx = Context.createFromMemory('', 'fake')
		# (x
		lexems = [('(','const',None), ('x','id',None), ('end','cmd',None)]
		with self.assertRaises(ErrorTaxon) as ex:
			node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		# 22)
		lexems = [('22','const','int'), (')','cmd',None), ('end','cmd',None)]
		with self.assertRaises(ErrorTaxon) as ex:
			node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(ex.exception.args[0], 'Invalid binary operation )')