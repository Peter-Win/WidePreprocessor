import unittest
from Wpp.WppCore import WppCore

class TestWppNew(unittest.TestCase):
	def testNoParams(self):
		source = """
class A
var a: A = A()
"""
		module = WppCore.createMemModule(source, 'new.wpp')
		a = module.findItem('a')
		self.assertEqual(a.type, 'var')
		av = a.getValueTaxon()
		self.assertEqual(av.type, 'new')

	def testSimpleParams(self):
		source = """
class Point
	field x: double
	field y: double
	constructor
		param x: double
		param y: double

var pt: Point = Point(1, 2)
"""
		module = WppCore.createMemModule(source, 'new.wpp')
		pt = module.findItem('pt')
		self.assertEqual(pt.type, 'var')
		ptVal = pt.getValueTaxon()
		self.assertEqual(ptVal.type, 'new')
