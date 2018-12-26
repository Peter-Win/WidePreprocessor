import unittest
from Wpp.WppExpression import WppExpression
from Wpp.Context import Context
from core.ErrorTaxon import ErrorTaxon

class TestWppExpression(unittest.TestCase):
	def testConst(self):
		ctx = Context.createFromMemory('', 'fake')
		taxon = WppExpression.create('2019', ctx)
		self.assertEqual(taxon.type, 'Const')
		self.assertEqual(taxon.constType, 'int')
		self.assertEqual(taxon.value, '2019')
		self.assertEqual(taxon.exportString(), '2019')

		taxon = WppExpression.create('-3.14', ctx)
		self.assertEqual(taxon.constType, 'fixed')
		self.assertEqual(taxon.value, '-3.14')
		self.assertEqual(taxon.exportString(), '-3.14')

		taxon = WppExpression.create('1.111e-06', ctx)
		self.assertEqual(taxon.constType, 'float')
		self.assertEqual(taxon.exportString(), '1.111E-06')

		taxon = WppExpression.create('"Hello!"', ctx)
		self.assertEqual(taxon.constType, 'string')
		self.assertEqual(taxon.exportString(), '"Hello!"')

		taxon = WppExpression.create('"First\\nSecond"', ctx)
		self.assertEqual(taxon.constType, 'string')
		self.assertEqual(taxon.value, 'First\nSecond')
		self.assertEqual(taxon.exportString(), '"First\\nSecond"')

		with self.assertRaises(ErrorTaxon) as ex:
			taxon = WppExpression.create('"Not closed', ctx)
		with self.assertRaises(ErrorTaxon) as ex:
			taxon = WppExpression.create('"Invalid slash\\"', ctx)
			