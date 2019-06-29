import unittest
from Wpp.WppCore import WppCore
from Wpp.WppLocalType import WppLocalType
from Wpp.Context import Context
from core.ErrorTaxon import ErrorTaxon

class TestWppType(unittest.TestCase):
	def testCreate(self):
		taxon = WppLocalType.create('MyType', Context.createFromMemory(''))
		self.assertEqual(taxon.type, 'TypeName')
		self.assertEqual(taxon.typeRef.name, 'MyType')

	def testNonTypeError(self):
		source = """
var public first: int
var public second: first
		"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Invalid type: Var')
		self.assertEqual(cm.exception.args[1][2], 'var public second: first')

	def testInvalidMatch(self):
		source = """
var public value: int
		"""