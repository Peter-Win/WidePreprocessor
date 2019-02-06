import unittest
import os
from Python.PyCore import PyCore
from Python.PyPackage import PyPackage
from Wpp.WppPackage import WppPackage
from out.deleteTree import deleteTree
from out.OutContextFolder import OutContextFolder

iniName = '__init__.py'

class TestPyPackage(unittest.TestCase):
	def testCreateTree(self):
		"""Тест создания иерархии пакетов"""
		path0 = os.path.split(__file__)[0]
		path0 = os.path.join(path0, 'files')
		pathDst = os.path.join(path0, 'dst')
		deleteTree(pathDst)
		def createPackage(name, items=[]):
			package = PyPackage()
			package.name = name
			[package.addNamedItem(i) for i in items]
			return package
		part11 = createPackage('part11')
		part1 = createPackage('part1', [part11])
		part2 = createPackage('part2')
		dst = createPackage('dst', [part1, part2])
		self.assertIn('part1', dst.dictionary)

		outContext = OutContextFolder(path0)
		self.assertFalse(os.path.isdir(pathDst))
		dst.export(outContext)
		self.assertTrue(os.path.isdir(pathDst))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, iniName)))
		self.assertTrue(os.path.isdir(os.path.join(pathDst, 'part1')))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, 'part1', iniName)))
		self.assertTrue(os.path.isdir(os.path.join(pathDst, 'part1', 'part11')))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, 'part1', 'part11', iniName)))

	def testCopyTree(self):
		""" Тест копирования иерархии """
		path0 = os.path.split(__file__)[0]
		path0 = os.path.join(path0, 'files')
		pathDst = os.path.join(path0, 'dst1')
		deleteTree(pathDst)
		self.assertFalse(os.path.isdir(pathDst))

		# Создать исходную иерархию
		pathSrc = os.path.join(path0, 'src1')
		if not os.path.exists(pathSrc):
			os.mkdir(pathSrc)
			os.mkdir(os.path.join(pathSrc, 'packageA'))
			os.mkdir(os.path.join(pathSrc, 'packageA', 'packageA1'))
			os.mkdir(os.path.join(pathSrc, 'packageA', 'packageA2'))
			os.mkdir(os.path.join(pathSrc, 'packageB'))
			os.mkdir(os.path.join(pathSrc, 'packageB', 'packageB1'))
			os.mkdir(os.path.join(pathSrc, 'packageB', 'packageB2'))
		src1 = WppPackage('src1')
		src1.read(pathSrc)
		self.assertIn('packageA', src1.dictionary)
		self.assertIn('packageB', src1.dictionary)
		self.assertIn('packageA1', src1.dictionary['packageA'].dictionary)

		# Создать иерархию для Python
		core = PyCore()
		dst1 = src1.clone(core)
		self.assertEqual(dst1.name, 'src1')
		dst1.name = 'dst1'
		self.assertEqual(dst1.type, 'Package')
		self.assertIn('packageA', dst1.dictionary)
		self.assertIn('packageB', dst1.dictionary)
		self.assertIn('packageA1', dst1.dictionary['packageA'].dictionary)

		outContext = OutContextFolder(path0)
		dst1.export(outContext)
		self.assertTrue(os.path.isdir(pathDst))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, iniName)))
		self.assertTrue(os.path.isdir(os.path.join(pathDst, 'packageA')))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, 'packageA', iniName)))
		self.assertTrue(os.path.isdir(os.path.join(pathDst, 'packageA', 'packageA1')))
		self.assertTrue(os.path.isfile(os.path.join(pathDst, 'packageA', 'packageA1', iniName)))
