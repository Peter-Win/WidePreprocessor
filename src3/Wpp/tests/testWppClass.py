import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

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
