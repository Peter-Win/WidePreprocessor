import unittest
from Wpp.WppTypeExpr import WppTypeExpr
from TS.TSCore import TSCore
from core.types.TaxonTypeExprName import TaxonTypeExprName
from Wpp.Context import Context

tsCore = TSCore.createInstance()

class TestTSTypeExprName(unittest.TestCase):
	def testClone(self):
		wppExpr = WppTypeExpr.parse('bool', Context.createFromMemory(''))
		self.assertEqual(wppExpr.type, TaxonTypeExprName.type)
