import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestLambda(unittest.TestCase):
	@unittest.skip('Wait for template, for, func type, lambda')
	def testSimple(self):
		source = """
func template calcSum: @Value
	param collection: Array @Item
	param callback: func const: @Value -> @Item
	var result: @Value = 0
	foreach collection => cell
		result += callback(cell)
	result

class A
	readonly mass: double
	constructor
		param init mass

func public main
	var sum1: int = calcSum([1, 2, 3], ===>)
		param item: int
		item
	
	var sum2: double = calcSum([A(1.1), A(2.2), A(3.3)], ===>)
		param a: A
		A.mass
		"""