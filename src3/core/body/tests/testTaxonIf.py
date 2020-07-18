import unittest
from core.body.TaxonIf import TaxonIf
from core.TaxonExpression import TaxonExpression
from core.body.TaxonBody import TaxonBody

class TestTaxonIf(unittest.TestCase):
	def testStructure(self):
		txif = TaxonIf()
		txif.addItem(TaxonExpression())
		txif.addItem(TaxonBody())
		txif.addItem(TaxonExpression())
		txif.addItem(TaxonBody())
		txif.addItem(TaxonBody())
		st = txif.getStructure()
		self.assertEqual(len(st), 3)
		self.assertEqual(st[0][0], 'if')
		self.assertIsInstance(st[0][1], TaxonExpression)
		self.assertIsInstance(st[0][2], TaxonBody)
		self.assertEqual(st[1][0], 'elif')
		self.assertIsInstance(st[1][1], TaxonExpression)
		self.assertIsInstance(st[1][2], TaxonBody)
		self.assertEqual(st[2][0], 'else')
		self.assertIsNone(st[2][1])
		self.assertIsInstance(st[2][2], TaxonBody)