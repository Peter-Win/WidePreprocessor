import unittest
from Wpp.WppCore import WppCore

#@unittest.skip('First need test TaxonCall')
class TestWppSuper(unittest.TestCase):
	def testSuperMethod(self):
		source = """
class public First
	method virtual calc: double
		param x: double
		x * 10
class public Second
	extends First
	method override calc: double
		param x: double
		super.calc(x) + 22
		"""
		module = WppCore.createMemModule(source, 'superMethod.fake')
