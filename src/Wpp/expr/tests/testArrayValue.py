import unittest
from Wpp.Context import Context
from Wpp.expr.scanLexems import scanLexems, createArray, optimizeStack

class TestArrayValue(unittest.TestCase):
	def testParse(self):
		ctx = Context.createFromMemory('', 'fake')
		lexems = [('[', 'cmd', None), ('1', 'const', 'int'), (',','cmd',None), ('2','const','int'), (']', 'cmd', None), ('end','cmd',None)]
		node, pos = createArray(lexems, 1, ctx)
		v, t, x = lexems[pos]
		self.assertEqual(t, 'cmd')
		self.assertEqual(v, 'end')
		self.assertEqual(node.export(), '[1, 2]')

		stack = [node]
		optimizeStack(stack, 100, ctx)
		self.assertEqual(len(stack), 1)

		node, pos = scanLexems(lexems, 0, {'end'}, ctx)
		self.assertEqual(node.export(), '[1, 2]')
