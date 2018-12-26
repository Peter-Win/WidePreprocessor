import unittest
from Taxon import Taxon
from TaxonDictionary import TaxonDictionary

class TestTaxonDictionary(unittest.TestCase):

	def testClone(self):
		class SrcDict(TaxonDictionary):
			def __init__(self):
				super().__init__()
				self.type = 'Dict'
		class SrcItem(Taxon):
			def __init__(self, name):
				super().__init__()
				self.type = 'Item'
				self.name = name
		class DstDict(TaxonDictionary):
			pass
		class DstItem(Taxon):
			def __str__(self):
				return '[' + self.name + ']'
		class DstCore:
			taxonMap = {'Dict': DstDict, 'Item': DstItem}
		# Исходная иерархия
		src = SrcDict()
		src.addNamedItem(SrcItem('Abc'))
		src.addNamedItem(SrcItem('Xyz'))
		src.addNamedItem(SrcItem('Iddqd'))
		self.assertEqual(src.dictionary['Abc'], src.items[0])
		self.assertEqual(src.type, 'Dict')
		# Клон
		dst = src.clone(DstCore())
		self.assertEqual(str(dst.dictionary['Xyz']), '[Xyz]')
		self.assertEqual(dst.dictionary['Iddqd'].type, 'Item')
		self.assertEqual(dst.type, 'Dict')
