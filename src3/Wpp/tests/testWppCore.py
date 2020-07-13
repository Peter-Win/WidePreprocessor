import unittest
from Wpp.WppCore import WppCore
from core.TaxonScalar import TaxonScalar

class TestWppCore(unittest.TestCase):
	def testScalar(self):
		core = WppCore.createInstance()
		typeInt = core.findItem('int')
		self.assertIsInstance(typeInt, TaxonScalar)
		self.assertEqual(typeInt.name, 'int')