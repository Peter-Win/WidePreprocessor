import unittest
from Wpp.parser.parseLexems import parseLexems
from Wpp.Context import Context

class TestParseLexems(unittest.TestCase):
	def testParse(self):
		ctx = Context.createFromMemory('')
		self.assertEqual(parseLexems('', ctx), [])
		self.assertEqual(parseLexems('A', ctx), [('A', 'id')])
		self.assertEqual(parseLexems('HelloWorld123', ctx), [('HelloWorld123', 'id')])
		self.assertEqual(parseLexems('size_t', ctx), [('size_t', 'id')])
		self.assertEqual(parseLexems('A B C', ctx), [('A', 'id'), ('B', 'id'), ('C', 'id')])
		self.assertEqual(parseLexems('123 456', ctx), [('123', 'int'), ('456', 'int')])
		self.assertEqual(parseLexems('12.3', ctx), [('12.3', 'fixed')])
		self.assertEqual(parseLexems('-45', ctx), [('-45', 'int')])
		self.assertEqual(parseLexems('[1, 2]', ctx), [('[', 'cmd'), ('1', 'int'), (',', 'cmd'), ('2', 'int'), (']', 'cmd')])
		self.assertEqual(parseLexems('-1.234E-06*x', ctx), [('-1.234E-06', 'float'), ('*', 'cmd'), ('x', 'id')])
		self.assertEqual(parseLexems('max(a, 1.5)', ctx), [('max', 'id'), ('(', 'cmd'), ('a', 'id'), (',','cmd'), ('1.5','fixed'), (')','cmd')])

	def testMultiCmd(self):
		ctx = Context.createFromMemory('')
		self.assertEqual(parseLexems('==', ctx), [('==', 'cmd')])
		self.assertEqual(parseLexems('<<>>', ctx), [('<<', 'cmd'), ('>>', 'cmd')])
