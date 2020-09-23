import unittest
from core.TaxonCore import TaxonCore

class TestFindBinOp(unittest.TestCase):
	def testUnsigned(self):
		core = TaxonCore.createInstance()
		sInt = core.findItem('int').buildQuasiType()
		uInt = core.findItem('int').buildQuasiType()
		uInt.attrs.add('unsigned')

		self.assertEqual(sInt.getDebugStr(), 'int')
		self.assertEqual(uInt.getDebugStr(), 'unsigned int')

		op, msg = core.findBinOp('+', sInt, sInt)
		self.assertIsNone(msg)
		self.assertEqual(op.type, 'declBinOp')
		self.assertEqual(op.opcode, '+')
		self.assertEqual(op.leftType.getDebugStr(), 'int')
		self.assertEqual(op.rightType.getDebugStr(), 'int')

		op, msg = core.findBinOp('+', uInt, uInt)
		self.assertIsNone(msg)
		self.assertEqual(op.leftType.getDebugStr(), 'unsigned int')
		self.assertEqual(op.rightType.getDebugStr(), 'unsigned int')

		op, msg = core.findBinOp('+', sInt, uInt)
		self.assertEqual(msg, 'Not found operator +(int, unsigned int)')
