import unittest
from Taxon import Taxon
from TaxonDictionary import TaxonDictionary
from core.ErrorTaxon import ErrorTaxon

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
		dst = src._clone(DstCore())
		self.assertEqual(str(dst.dictionary['Xyz']), '[Xyz]')
		self.assertEqual(dst.dictionary['Iddqd'].type, 'Item')
		self.assertEqual(dst.type, 'Dict')

	def testFindUpPath(self):
		"""
		  +root+
		  |    |
		left  right
		|  |  |  |
		A  B  C  D
		"""
		def add(owner, name):
			return owner.addNamedItem(TaxonDictionary(name))
		root = TaxonDictionary('root')
		left = add(root, 'left')
		right = add(root, 'right')
		a = add(left, 'A')
		b = add(left, 'B')
		c = add(right, 'C')
		d = add(right, 'D')
		self.assertEqual(a.findUpPath('left').name, left.name)
		self.assertEqual(a.findUpPath('left.B'), b)
		self.assertEqual(a.findUpPath('root.right.C'), c)
		with self.assertRaises(ErrorTaxon) as cm:
			a.findUpPath('root.right.E')
		self.assertEqual(str(cm.exception), '*Error* Taxon root.right doesn\'t contain field "E"')
