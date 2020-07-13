import unittest
from Taxon import Taxon

class SrcA(Taxon):
	type = 'A'

class SrcB(Taxon):
	type = 'B'

class SrcCore(Taxon):
	taxonMap = {'A': SrcA, 'B': SrcB}

class DstA(Taxon):
	type = 'A'
	def getDebugStr(self):
		return 'DstA_' + self.name

class DstB(Taxon):
	type = 'B'
	def getDebugStr(self):
		return 'DstB_' + self.name

class DstCore(Taxon):
	taxonMap = {'A': DstA, 'B': DstB}


class TestTaxon(unittest.TestCase):
	def testCloneAll(self):
		srcCore = SrcCore()
		srcCore.core = srcCore
		a1 = SrcA('A1')
		a1.attrs.add('public')
		srcCore.addItem(a1)
		b1 = SrcB('B1')
		b1.attrs.add('static')
		a1.addItem(b1)
		dstCore = DstCore()
		dstCore.core = dstCore

		a1.cloneAll(dstCore)
		self.assertEqual(len(dstCore.items), 1)
		dstA1 = dstCore.items[0]
		self.assertEqual(dstA1.type, 'A')
		self.assertEqual(dstA1.name, 'A1')
		self.assertEqual(dstA1.attrs, set(['public']))
		self.assertEqual(dstA1.getDebugStr(), 'DstA_A1')
		self.assertEqual(len(dstA1.items), 1)

		dstB1 = dstA1.items[0]
		self.assertEqual(dstB1.type, 'B')
		self.assertEqual(dstB1.name, 'B1')
		self.assertEqual(dstB1.attrs, set(['static']))
		self.assertEqual(dstB1.getDebugStr(), 'DstB_B1')

	def testGetOwners(self):
		srcCore = SrcCore()
		a = SrcA('A')
		b = SrcB('B')
		srcCore.addItem(a)
		a.addItem(b)
		owners = b.getOwners()
		self.assertEqual(len(owners), 3)
		self.assertEqual(owners[0], b)
		self.assertEqual(owners[1], a)
		self.assertEqual(owners[2], srcCore)

	def testGetPathExt(self):
		from Wpp.WppCore import WppCore
		from TaxonDict import TaxonDict
		module = WppCore.createMemModule('', 'empty.mem')
		noname0 = module.addItem(TaxonDict())
		noname1 = module.addItem(TaxonDict())
		a = noname1.addItem(TaxonDict('A'))
		b = a.addItem(Taxon('B'))
		path = b.getPathExt()
		self.assertEqual(path, ['@root', 1, 'A', 'B'])
		# second case - object in core
		txInt = module.core.findItem('int')
		path = txInt.getPathExt()
		self.assertEqual(path, ['int'])
