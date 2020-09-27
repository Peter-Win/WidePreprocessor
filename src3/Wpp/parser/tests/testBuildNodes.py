import unittest
from Wpp.Context import Context
from Wpp.parser.parseLexems import parseLexems
from Wpp.parser.buildNodes import buildNodes

def testCvt(code):
	""" parse and convert to debud string """
	ctx = Context.createFromMemory(code)
	lexems = parseLexems(code, ctx)
	lexems.append(('END', 'cmd'))
	node, pos = buildNodes(lexems, 0, {'END'}, ctx)
	return str(node)


class TestBuildNodes(unittest.TestCase):
	def testSingleArg(self):
		self.assertEqual(testCvt('1'), 'const:1')
		self.assertEqual(testCvt('-1'), 'const:-1')
		self.assertEqual(testCvt('1.23'), 'const:1.23')
		self.assertEqual(testCvt('-1.23E-06'), 'const:-1.23E-06')

		self.assertEqual(testCvt('true'), 'const:true')
		self.assertEqual(testCvt('false'), 'const:false')
		self.assertEqual(testCvt('null'), 'const:null')

		self.assertEqual(testCvt('x'), 'named:x')
		self.assertEqual(testCvt('this'), 'named:this')

	def testBinOp(self):
		self.assertEqual(testCvt('1 + x'), 'binop:+(const:1, named:x)')
		self.assertEqual(testCvt('this.flag'), 'binop:.(named:this, named:flag)')
		self.assertEqual(testCvt('a * b + c'), 'binop:+(binop:*(named:a, named:b), named:c)')
		self.assertEqual(testCvt('a + b * c'), 'binop:+(named:a, binop:*(named:b, named:c))')
		self.assertEqual(testCvt('a + b - c'), 'binop:-(binop:+(named:a, named:b), named:c)')
		self.assertEqual(testCvt('x = y + z'), 'binop:=(named:x, binop:+(named:y, named:z))')

	def testCall(self):
		self.assertEqual(testCvt('myFunc()'), 'call:call(named:myFunc)')
		self.assertEqual(testCvt('myFunc(45)'), 'call:call(named:myFunc, const:45)')
		self.assertEqual(testCvt('myFunc(a, b, c)'), 'call:call(named:myFunc, named:a, named:b, named:c)')
		self.assertEqual(testCvt('myFunc(x + 1.2)'), 'call:call(named:myFunc, binop:+(named:x, const:1.2))')
		self.assertEqual(testCvt('a(x) + b(y)'), 'binop:+(call:call(named:a, named:x), call:call(named:b, named:y))')
		self.assertEqual(testCvt('sqrt(sqr(x) + sqr(y))'), 'call:call(named:sqrt, binop:+(call:call(named:sqr, named:x), call:call(named:sqr, named:y)))')
		self.assertEqual(testCvt('root.obj.fun(x, y)'), 'call:call(binop:.(binop:.(named:root, named:obj), named:fun), named:x, named:y)')
		self.assertEqual(testCvt('One() + 20'), 'binop:+(call:call(named:One), const:20)')
