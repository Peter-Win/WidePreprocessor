import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore

class TestPyType(unittest.TestCase):
	def testCoreTypes(self):
		source = 'var num: int = 22'
		srcModule = WppCore.createMemModule(source, 'types.fake')
		num = srcModule.dictionary['num']
		localType = num.getLocalType()
		self.assertEqual(localType._typeName, None)
		self.assertIn('type', localType.refs)
		typeDecl = localType.getTypeTaxon()
		self.assertIsNotNone(typeDecl)

		pyCore = PyCore()
		dstModule = srcModule.cloneRoot(pyCore)
		self.assertIn('num', dstModule.dictionary)
		num = dstModule.dictionary['num']
		self.assertEqual(num.type, 'Var')
		localType = num.getLocalType()
		self.assertEqual(localType.type, 'TypeName')
		self.assertIn('type', localType.refs)
		typeDecl = localType.getTypeTaxon()
		self.assertIsNotNone(typeDecl)