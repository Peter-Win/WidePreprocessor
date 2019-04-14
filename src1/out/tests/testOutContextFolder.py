import unittest
import os
from out.OutContextFolder import OutContextFolder
from out.deleteTree import deleteTree

modulePath = os.path.dirname(__file__)
testPath = os.path.join(modulePath, 'files')

class TestOutContextFolder(unittest.TestCase):
	def testCreateFolder(self):
		deleteTree(testPath)
		baseFolder = OutContextFolder(modulePath)
		filesFolder = baseFolder.createFolder('files')
		subFolder = filesFolder.createFolder('subFolder')
		self.assertTrue(os.path.isdir(testPath))
		self.assertTrue(os.path.isdir(os.path.join(testPath, 'subFolder')))

	def testCreateFile(self):
		filesFolder = OutContextFolder(testPath)
		f1 = filesFolder.createFile('first.txt')
		f1.writeln('Hello!')
		f1.close()
		self.assertTrue(os.path.isfile(os.path.join(testPath, 'first.txt')))
		self.assertEqual(f1.fileName, os.path.join(testPath, 'first.txt'))
