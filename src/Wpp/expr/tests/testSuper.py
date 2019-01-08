import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

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
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())


	def testSuperConstructor(self):
		source = """
class public A
	field count: int
	constructor public
		param init count

class public B
	extends A
	field year: int
	constructor public
		param count: int
		param init year
		super(count)
		"""
		module = WppCore.createMemModule(source, 'testSuperConstructor.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
