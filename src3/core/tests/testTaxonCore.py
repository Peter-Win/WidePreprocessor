import unittest
from core.TaxonCore import TaxonCore
from Taxon import Taxon
from TaxonDict import TaxonDict
from core.TaxonExpression import TaxonConst
from core.QuasiType import QuasiType
from core.TaxonTypeExpr import TaxonTypeExpr

class TestTaxonCore(unittest.TestCase):
	def testCreateInstance(self):
		core = TaxonCore.createInstance()
		self.assertEqual(core.type, 'core')

	def testResolveTasks(self):
		core = TaxonCore.createInstance()
		class MyTaxon(Taxon):
			def __init__(self, name=''):
				super().__init__(name)
				self.ready = False
		taxonA = core.addItem(MyTaxon('A'))
		taxonB = core.addItem(MyTaxon('B'))
		queue = []
		class TaskA:
			def check(self):
				return taxonB.ready
			def exec(self):
				self.taxon.ready = True
				queue.append(self.taxon.name)
		class TaskB(TaskA):
			def check(self):
				return True

		taxonA.addTask(TaskA())
		taxonB.addTask(TaskB())
		core.resolveTasks()
		self.assertEqual(len(core.tasks), 0)
		self.assertEqual(queue, ['B', 'A'])
		self.assertTrue(taxonA.ready)
		self.assertTrue(taxonB.ready)

	def testFindByPathExt(self):
		core = TaxonCore.createInstance()
		module = core.setRoot(TaxonDict('testRoot'))
		subModuleA = module.addItem(Taxon('subModuleA'))
		subModuleB = module.addItem(Taxon('subModuleB'))
		noname0 = subModuleB.addItem(Taxon())
		noname1 = subModuleB.addItem(TaxonDict())
		itemA = noname1.addItem(Taxon('A'))
		itemB = noname1.addItem(Taxon('B'))
		pathB = itemB.getPathExt()
		self.assertEqual(pathB, ['@root', 'subModuleB', 1, 'B'])
		self.assertEqual(core.findByPathExt(pathB), itemB)

		self.assertEqual(core.findByPathExt(['float']), core.findItem('float'))

	def testFindUp(self):
		core = TaxonCore.createInstance()
		module = core.setRoot(TaxonDict('testRoot'))
		tInt = module.startFindUp('double')
		self.assertEqual(tInt.name, 'double')
		self.assertTrue(tInt.isType())

	def testSizeT(self):
		core = TaxonCore.createInstance()
		size_t = core.findItem('size_t')
		self.assertEqual(size_t.type, 'typedef')
		self.assertEqual(len(size_t.items), 1)
		sizetExpr = size_t.getTypeExpr()
		self.assertIsInstance(sizetExpr, TaxonTypeExpr)

		constA = TaxonConst('int', 123, '123')
		res, errMsg = QuasiType.matchTaxons(size_t, constA)
		self.assertIsNone(errMsg)
		self.assertEqual(res, 'constExact')

		constB = TaxonConst('int', -1, '-1')
		res, errMsg = QuasiType.matchTaxons(size_t, constB)
		self.assertEqual(errMsg, 'Invalid conversion of negative value "-1" to "unsigned long"')

