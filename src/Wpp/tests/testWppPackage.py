import unittest
import os
from Wpp.WppPackage import WppPackage
from out.deleteTree import deleteTree
from out.OutContextFolder import OutContextFolder

class TestWppPackage(unittest.TestCase):
	def setUp(self):
		folder22Path = os.path.join(os.path.dirname(__file__), 'packageTest', 'folder2', 'folder22')
		if not os.path.exists(folder22Path):
			os.mkdir(folder22Path)
	def testRead(self):
		root = WppPackage('packageTest')
		self.assertEqual(root.type, 'Package')
		root.read(os.path.join(os.path.dirname(__file__), root.name))
		self.assertIn('folder1', root.dictionary)
		self.assertIn('folder2', root.dictionary)
		folder1 = root.dictionary['folder1']
		self.assertIn('folder11', folder1.dictionary)
		self.assertIn('folder12', folder1.dictionary)
		folder2 = root.dictionary['folder2']
		self.assertIn('folder21', folder2.dictionary)
		self.assertIn('folder22', folder2.dictionary)

		self.assertIn('A', root.dictionary)
		self.assertEqual(root.dictionary['A'].name, 'A')

	def testExport(self):
		root = WppPackage('packageTest')
		root.read(os.path.join(os.path.dirname(__file__), root.name))
		root.fullUpdate()

		exportRoot = os.path.join(os.path.dirname(__file__), 'exportTest')
		deleteTree(exportRoot)
		os.mkdir(exportRoot)

		outContext = OutContextFolder(exportRoot)
		root.export(outContext)
		folder1 = os.path.join(exportRoot, root.name, 'folder1')
		folder11 = os.path.join(folder1, 'folder11')
		self.assertTrue(os.path.isdir(folder1))
		self.assertTrue(os.path.isdir(folder11))
		folder22 = os.path.join(exportRoot, root.name, 'folder2', 'folder22')
		self.assertTrue(os.path.isdir(folder22))
