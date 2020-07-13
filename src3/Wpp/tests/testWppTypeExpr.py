import unittest
from Wpp.WppTypeExpr import WppTypeExpr
from Wpp.Context import Context

class TestWppTypeExpr(unittest.TestCase):
	def testSimpleName(self):
		context = Context.createFromMemory('unsigned int')
		taxon = WppTypeExpr.parse(context.readLine(), context)

		self.assertEqual(taxon.type, '@typeExprName')
		self.assertEqual(taxon.typeName, 'int')
		self.assertEqual(taxon.attrs, set(['unsigned']))

	def testArray(self):
		context = Context.createFromMemory('Array String')
		taxon = WppTypeExpr.parse(context.readLine(), context)
		self.assertEqual(taxon.type, '@typeExprArray')

		itemTaxon = taxon.getItemTaxon()
		self.assertEqual(itemTaxon.type, '@typeExprName')
		self.assertEqual(itemTaxon.typeName, 'String')

