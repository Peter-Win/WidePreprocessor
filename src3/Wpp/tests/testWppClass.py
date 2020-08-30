import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream
from core.QuasiType import QuasiType

class TestWppClass(unittest.TestCase):
	def testSimple(self):
		source = """
class public simple Point
	# 2D coordinates
	field public x: double
	field public y: double
	method isValid: bool
		if x
			return true
		if y
			return true
		return false
"""
		module = WppCore.createMemModule(source, 'simple.wpp')
		point = module.findItem('Point')
		self.assertEqual(point.type, 'class')
		self.assertEqual(point.name, 'Point')
		self.assertEqual(point.attrs, {'public', 'simple'})
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), WppCore.strPack(source))

	def testMatch(self):
		source = """
class public First

class public Second

var first: First
var firstA: First
var second: Second
"""
		module = WppCore.createMemModule(source, 'simple.wpp')
		First = module.findItem('First')
		Second = module.findItem('Second')
		first = module.findItem('first')
		firstA = module.findItem('firstA')
		second = module.findItem('second')
		self.assertEqual(QuasiType.matchTaxons(first, First), ('exact', None))
		self.assertEqual(QuasiType.matchTaxons(firstA, First), ('exact', None))
		self.assertEqual(QuasiType.matchTaxons(first, firstA), ('exact', None))
		self.assertEqual(QuasiType.matchTaxons(firstA, first), ('exact', None))
		self.assertEqual(QuasiType.matchTaxons(second, Second), ('exact', None))
		self.assertEqual(QuasiType.matchTaxons(first, Second), (None, 'Cannot convert from "class Second" to "var first: First"'))
