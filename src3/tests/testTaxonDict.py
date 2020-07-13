import unittest
from TaxonDict import TaxonDict

class TestTaxonDict(unittest.TestCase):
	def testAddItem(self):
		first = TaxonDict('first')
		second = TaxonDict('second')
		owner = TaxonDict()
		owner.addItem(first)
		owner.addItem(second)
		self.assertEqual(owner.dict, {'first': first, 'second': second})

	def testClone(self):
		class Node(TaxonDict):
			type = 'Node'
		class Core(TaxonDict):
			taxonMap = {'Node': Node}
		srcCore = Core('srcCore')
		srcCore.core = srcCore
		dstCore = Core('dstCore')
		dstCore.core = dstCore

		srcRoot = srcCore.addItem(Node('Root'))
		srcLeft = srcRoot.addItem(Node('Left'))
		srcRight = srcRoot.addItem(Node('Right'))

		dstRoot = srcRoot.clone(dstCore)
		self.assertIn('Left', dstRoot.dict)
		self.assertIn('Right', dstRoot.dict)
		self.assertEqual(len(dstRoot.dict), 2)
		dstLeft = dstRoot.dict['Left']
		dstRight = dstRoot.dict['Right']
		self.assertEqual(dstLeft.name, 'Left')
		self.assertEqual(dstRight.name, 'Right')

		# Изменение словаря dstRoot не должно повлиять на srcRoot
		dstRoot.addItem(Node('Middle'))
		self.assertEqual(len(dstRoot.dict), 3)
		self.assertEqual(len(srcRoot.dict), 2)
