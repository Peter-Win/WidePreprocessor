import unittest
from core.TaxonScalar import TaxonScalar
from core.TaxonExpression import TaxonConst
from core.QuasiType import QuasiType

tmap = {prop[0]:TaxonScalar(prop) for prop in TaxonScalar.propsList}
qIntConst = TaxonConst('int', 2500).buildQuasiType()
qIntConstNeg = TaxonConst('int', -123).buildQuasiType()
qFloatConst = TaxonConst('float', 3.14).buildQuasiType()
qLongConst = TaxonConst('int', 2147483650).buildQuasiType()
qDoubleConst = TaxonConst('float', 3.5E+38).buildQuasiType()

class TestTaxonScalar(unittest.TestCase):
	def testIntConst(self):
		txInt = tmap['int']
		self.assertIsInstance(txInt, TaxonScalar)
		self.assertEqual(txInt.name, 'int')
		qInt = txInt.buildQuasiType()

		# int value = 2500
		result, errMsg = txInt.matchQuasiType(qInt, qIntConst)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'constExact')

		# int value = -123
		result, errMsg = txInt.matchQuasiType(qInt, qIntConstNeg)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'constExact')

		# cant match too large value
		result, errMsg = txInt.matchQuasiType(qInt, qLongConst)
		self.assertIsNone(result)
		self.assertEqual(errMsg, 'The value "2147483650" is outside the range of "int"')

	def testLongConst(self):
		txLong = tmap['long']
		qULong = txLong.buildQuasiType()
		qULong.update({'unsigned'})
		self.assertIsInstance(qULong, QuasiType)
		self.assertEqual(qULong.taxon.name, 'long')
		self.assertIn('unsigned', qULong.attrs)
		self.assertEqual(qULong.getDebugStr(), 'unsigned long')

		# unsigned long value = 25
		result, errMsg = txLong.matchQuasiType(qULong, qIntConst)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'constExact')

		# unsigned long value can't match -123 !
		result, errMsg = txLong.matchQuasiType(qULong, qIntConstNeg)
		self.assertIsNone(result)
		self.assertEqual(errMsg, 'Invalid conversion of negative value "-123" to "unsigned long"')

	def testFloatConst(self):
		txFloat = tmap['float']
		qFloat = txFloat.buildQuasiType()

		result, errMsg = txFloat.matchQuasiType(qFloat, qFloatConst)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'constExact')

		result, errMsg = txFloat.matchQuasiType(qFloat, qIntConstNeg)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'constUpcast')

		result, errMsg = txFloat.matchQuasiType(qFloat, qDoubleConst)
		self.assertIsNone(result)
		self.assertEqual(errMsg, 'The value "3.5e+38" is outside the range of "float"')

	def testVarToVar(self):
		txInt = tmap['int']
		txLong = tmap['long']
		txFloat = tmap['float']
		txDouble = tmap['double']
		qInt = txInt.buildQuasiType()
		qLong = txLong.buildQuasiType()
		qFloat = txFloat.buildQuasiType()
		qDouble = txDouble.buildQuasiType()

		# int
		result, errMsg = txInt.matchQuasiType(qInt, qInt)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'exact')

		result, errMsg = txInt.matchQuasiType(qInt, qLong)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

		result, errMsg = txInt.matchQuasiType(qInt, qFloat)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

		# long
		result, errMsg = txLong.matchQuasiType(qLong, qLong)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'exact')

		result, errMsg = txLong.matchQuasiType(qLong, qInt)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'upcast') # convert int to long is upcast

		result, errMsg = txLong.matchQuasiType(qLong, qDouble)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

		# float
		result, errMsg = txFloat.matchQuasiType(qFloat, qFloat)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'exact')

		result, errMsg = txFloat.matchQuasiType(qFloat, qDouble)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

		result, errMsg = txFloat.matchQuasiType(qFloat, qInt)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

		# double
		result, errMsg = txDouble.matchQuasiType(qDouble, qDouble)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'exact')

		result, errMsg = txDouble.matchQuasiType(qDouble, qFloat)
		self.assertIsNone(errMsg)
		self.assertEqual(result, 'upcast')

		result, errMsg = txDouble.matchQuasiType(qDouble, qInt)
		self.assertIsNone(errMsg) # Use standard message about type mismatch
		self.assertIsNone(result)

