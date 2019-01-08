import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppArray(unittest.TestCase):
	def testDecl(self):
		source = """
var public myArray: Array int	
		"""
		module = WppCore.createMemModule(source, 'arrayDecl.fake')
		myArray = module.dictionary['myArray']
		self.assertEqual(myArray.type, 'Var')
		localType = myArray.getLocalType()
		self.assertEqual(localType.type, 'TypeArray')
		itemType = localType.getItemType()
		self.assertEqual(itemType.type, 'TypeName')
		self.assertEqual(itemType.exportString(), 'int')
		self.assertEqual(module.core, itemType.core)

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	#@unittest.skip('Wait for scanLexems')
	def testInit(self):
		""" Массив с инициализацией """
		source = """
var public nums: Array String = ["First", "Second", "Third"]
		"""
		module = WppCore.createMemModule(source, 'arrayInit.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
