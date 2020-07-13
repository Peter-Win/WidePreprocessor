import unittest
from Wpp.WppCore import WppCore
from Wpp.WppVar import WppVar
from Wpp.WppModule import WppModule
from core.TaxonTypeExpr import TaxonTypeExpr
from Wpp.types.WppTypeExprName import WppTypeExprName
from Wpp.WppExpression import WppConst

class TestWppVar(unittest.TestCase):

	def testCreateInstance(self):
		core = WppCore.createInstance()
		inst = core.creator('var')('varName')
		self.assertEqual(inst.type, 'var')
		self.assertEqual(inst.name, 'varName')

	def testParseHead(self):
		err, name, attrs, stype, sval = WppVar.parseHead('var public const myPi: double = 3.14')
		self.assertIsNone(err)
		self.assertEqual(name, 'myPi')
		self.assertEqual(attrs, {'public', 'const'})
		self.assertEqual(stype, 'double')
		self.assertEqual(sval, '3.14')

	def testMin(self):
		source = "var myName: int"
		module = WppCore.createMemModule(source, "min.mem")
		self.assertIsInstance(module, WppModule)
		self.assertEqual(len(module.items), 1)
		self.assertEqual(len(module.dict), 1)

		txMyName = module.findItem('myName')
		self.assertIsInstance(txMyName, WppVar)
		self.assertEqual(len(txMyName.items), 1)

		self.assertIsNone(txMyName.getValueTaxon())
		txMyType = txMyName.getTypeTaxon()
		self.assertIsInstance(txMyType, TaxonTypeExpr)
		self.assertIsInstance(txMyType, WppTypeExprName)
		self.assertEqual(txMyType.typeName, 'int')

		qtype = txMyType.buildQuasiType()
		self.assertEqual(qtype.taxon.name, 'int')

	def testWithInitialValue(self):
		source = 'var const myPi: double = 3.14'
		module = WppCore.createMemModule(source, "varinit.mem")
		txVar = module.findItem('myPi')
		self.assertIsInstance(txVar, WppVar)
		txValue = txVar.getValueTaxon()
		self.assertIsInstance(txValue, WppConst)

