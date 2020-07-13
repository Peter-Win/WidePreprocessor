import unittest
from Taxon import Taxon
from core.TaxonRef import TaxonRef
from Wpp.WppCore import WppCore
from core.TaxonCore import TaxonCore
from core.TaxonScalar import TaxonScalar
from core.TaxonTypedef import TaxonTypedef
from core.types.TaxonTypeExprName import TaxonTypeExprName


class DstCore(TaxonCore):
	def init(self):
		from core.buildCoreTaxonsMap import buildCoreTaxonsMap
		self.taxonMap = buildCoreTaxonsMap()
		super().init()


class TestTaxonRef(unittest.TestCase):
	def testCloneRefToCoreObject(self):
		""" Clone reference to internal core object """
		srcModule = WppCore.createMemModule('', 'hello')
		srcCore = srcModule.core
		srcDouble = srcCore.findItem('double')
		self.assertEqual(srcDouble.name, 'double')
		srcRef = srcModule.addItem(TaxonRef())
		srcRef.setTarget(srcDouble) # source reference to double

		dstCore = DstCore.createInstance()
		dstDouble = dstCore.findItem('double')
		self.assertIsNot(srcDouble, dstDouble)
		dstModule = dstCore.setRoot(Taxon('hello'))
		dstRef = dstModule.addItem(srcRef.clone(dstModule))
		self.assertIsInstance(dstRef, TaxonRef)
		self.assertIs(dstRef.core, dstCore)
		self.assertIsNot(srcRef, dstRef)
		self.assertEqual(dstRef.path, srcDouble.getPathExt())
		self.assertIsNone(dstRef.target)

		# init reference
		dstModule.initAllRefs()
		self.assertIsInstance(dstRef.target, TaxonScalar)
		self.assertEqual(dstRef.target.name, 'double')
		self.assertIsNot(dstRef.target, srcDouble)
		self.assertIs(dstRef.target, dstDouble)

