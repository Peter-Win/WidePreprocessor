import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.Signature import Signature

class TestSignature(unittest.TestCase):
	def testConst(self):
		source = """
func test: bool
	param x: int
	x != 0
func test: bool
	param s: String
	s != ""
var public res1: bool = test(10)
var public res2: bool = test("ABC")
var i: int
var public res3: bool = test(i)
		"""
		module = WppCore.createMemModule(source, 'const.fake')
		testOver = module.dictionary['test']
		self.assertEqual(testOver.type, 'Overloads')
		self.assertEqual(len(testOver.items), 2)
		testInt = testOver.items[0]
		testStr = testOver.items[1]

		res1 = module.dictionary['res1']
		v = res1.getValueTaxon()
		self.assertEqual(v.type, 'Call')
		sign = Signature.createFromCall(v)
		self.assertEqual(str(sign), '10 => bool')
		sum = sign.match(testStr)
		self.assertEqual(sum, 0)
		sum = sign.match(testInt)
		self.assertGreater(sum, 0)

		res2 = module.dictionary['res2']
		sign = Signature.createFromCall(res2.getValueTaxon())
		self.assertEqual(str(sign), '"ABC" => bool')
		sum = sign.match(testStr)
		self.assertGreater(sum, 0)
		sum = sign.match(testInt)
		self.assertEqual(sum, 0)

		res3 = module.dictionary['res3']
		sign = Signature.createFromCall(res3.getValueTaxon())
		self.assertEqual(str(sign), 'int => bool')

	def testMethods(self):
		source = """
class Adder
	field info: String = ""
	method add
		param value: String
		info += value
	method add
		param value: double
		info += String(value)
	method add
		param x: double
		param y: double
		info += "{" + String(x) + "," + String(y) + "}"
	method add
		param a: Adder
		info += a.info
	method hello
		add(1)
		add("; ")
		add(3.14)
		add("; ")
		add(1, 2.3)
	method hello2
		param a: Adder
		add(a)
		"""
		module = WppCore.createMemModule(source, 'method.fake')
		classA = module.dictionary['Adder']
		addOver = classA.dictionary['add']
		self.assertEqual(len(addOver.items), 4)
		addStr, addDbl, addDbl2, addA = addOver.items
		body = classA.dictionary['hello'].items[0].getBody().items
		sign = Signature.createFromCall(body[0])
		self.assertEqual(str(sign), '1')
		cmd = body[1]
		self.assertEqual(cmd.type, 'Call')
		sign = Signature.createFromCall(cmd)
		self.assertEqual(str(sign), '"; "')
		sign = Signature.createFromCall(body[2])
		self.assertEqual(str(sign), '3.14')
		sign = Signature.createFromCall(body[4])
		self.assertEqual(str(sign), '1; 2.3')
		self.assertGreater(sign.match(addDbl2), 0)
		self.assertEqual(sign.match(addDbl), 0)

		body = classA.dictionary['hello2'].items[0].getBody().items
		call = body[0]
		self.assertEqual(call.type, 'Call')
		sign = Signature.createFromCall(call)
		self.assertEqual(classA.matchQuasi(sign.params[0]), 'exact')
		self.assertEqual(str(sign), 'Adder')
		self.assertGreater(sign.match(addA), 0)

		self.assertEqual(call.getCaller().type, 'IdExpr')
		self.assertEqual(call.getCaller().getDeclaration().type, 'Overloads')
		self.assertEqual(call.getDeclaration(), addA)

	def testBool(self):
		source = """
func test: bool
	param first: bool
	param second: bool = false
	first || second
func public main
	var a: bool = test(true)
	var b: bool = test(false, true)
	var c: bool = test(a, b)
		"""
		module = WppCore.createMemModule(source, 'bool.fake')
		test0 = module.dictionary['test'].items[0]
		main = module.dictionary['main'].items[0]
		a, b, c = [cmd.getValueTaxon() for cmd in main.getBody().items]
		self.assertEqual(a.type, 'Call')
		sign = Signature.createFromCall(a)
		self.assertEqual(str(sign), 'true => bool')
		self.assertGreater(sign.match(test0), 0)

		sign = Signature.createFromCall(b)
		self.assertEqual(str(sign), 'false; true => bool')
		self.assertGreater(sign.match(test0), 0)
		sign = Signature.createFromCall(c)
		self.assertEqual(str(sign), 'bool; bool => bool')
		self.assertGreater(sign.match(test0), 0)
