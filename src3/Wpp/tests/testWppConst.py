import unittest
from Wpp.WppExpression import WppExpression, WppConst
from Wpp.WppCore import WppCore
from Wpp.Context import Context

class TestWppConst(unittest.TestCase):
	def testCreate(self):
		core = WppCore.createInstance()
		taxon = core.creator(WppConst.type)('null')
		self.assertIsInstance(taxon, WppConst)
		self.assertEqual(taxon.constType, 'null')

	def testConstParse(self):
		ctx = Context.createFromMemory('')
		c = WppExpression.parse('25', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'int')
		self.assertEqual(c.value, 25)
		self.assertTrue(c.isNumber())

		c = WppExpression.parse('-8', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'int')
		self.assertEqual(c.value, -8)

		c = WppExpression.parse('3.14', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'fixed')
		self.assertEqual(c.value, 3.14)
		self.assertTrue(c.isNumber())

		c = WppExpression.parse('-1.1E-4', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'float')
		self.assertEqual(c.value, -0.00011)

		c = WppExpression.parse('true', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'bool')
		self.assertEqual(c.value, True)
		self.assertFalse(c.isNumber())

		c = WppExpression.parse('false', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'bool')
		self.assertEqual(c.value, False)
		self.assertFalse(c.isNumber())

		c = WppExpression.parse('null', ctx)
		self.assertEqual(c.type, WppConst.type)
		self.assertEqual(c.constType, 'null')
		self.assertEqual(c.value, None)
		self.assertFalse(c.isNumber())

	def testQuasiType(self):
		c = WppConst('int', 1234)
		qt = c.buildQuasiType()
		self.assertEqual(qt.taxon, c)
