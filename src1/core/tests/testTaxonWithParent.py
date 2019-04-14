import unittest
from core.TaxonWithParent import TaxonWithParent
from core.TaxonModule import TaxonModule
from core.TaxonClass import TaxonClass
from core.TaxonInterface import TaxonInterface
from core.Ref import Ref

class TestTaxonWithParent(unittest.TestCase):
	def testUpcastTo(self):
		module = TaxonModule('module')
		classA = module.addNamedItem(TaxonClass('A'))
		classB = module.addNamedItem(TaxonClass('B'))
		classB.parent = Ref('A', classA)
		classC = module.addNamedItem(TaxonClass('C'))
		classC.parent = Ref('B', classB)
		intAx = module.addNamedItem(TaxonInterface('Ax'))
		intBx = module.addNamedItem(TaxonInterface('Bx'))
		intBx.parent = Ref('Ax', intAx)
		intCx = module.addNamedItem(TaxonInterface('Cx'))
		classC.implements.append(Ref('Bx', intBx))
		classC.implements.append(Ref('Cx', intCx))
		self.assertTrue(classC.canUpcastTo(classC))
		self.assertTrue(classC.canUpcastTo(classB))
		self.assertTrue(classC.canUpcastTo(classA))
		self.assertTrue(classB.canUpcastTo(classB))
		self.assertFalse(classA.canUpcastTo(classB))

		self.assertFalse(classA.canUpcastTo(intAx))
		self.assertFalse(classB.canUpcastTo(intBx))

		self.assertTrue(intAx.canUpcastTo(intAx))
		self.assertTrue(intBx.canUpcastTo(intAx))
		self.assertFalse(intCx.canUpcastTo(intAx))

		self.assertTrue(classC.canUpcastTo(intCx))
		self.assertTrue(classC.canUpcastTo(intBx))
		self.assertTrue(classC.canUpcastTo(intAx))
