import unittest
import os
from Taxon import Taxon
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppCore import WppCore

def taxonEx(type, items=[]):
	res = Taxon()
	res.type = type
	[res.addItem(i) for i in items]
	return res

class TestTaxon(unittest.TestCase):
	def testThrowError(self):
		""" Тест генерации ошибки """
		taxon = Taxon()
		taxon.location = ('file.wpp', 22, 'Some text...')
		with self.assertRaises(RuntimeError) as cm:
			taxon.throwError('Hello')
		self.assertEqual(str(cm.exception), '*Error* Hello in file file.wpp, line 22: Some text...')
		fileName, lineNumber, string = cm.exception.args[1]
		self.assertEqual(fileName, 'file.wpp')
		self.assertEqual(lineNumber, 22)
		self.assertEqual(string, 'Some text...')

	def testClone(self):
		class TaxonSrc(Taxon):
			def __init__(self, name):
				super().__init__()
				self.type = 'Test'
				self.name = name
		class TaxonDst(Taxon):
			def __str__(self):
				return self.name + '(' + ', '.join([str(i) for i in self.items]) + ')'
		class CoreDst:
			taxonMap = {'Test': TaxonDst}
		# Source hierarchy A -> B, C
		a = TaxonSrc('A')
		a.attrs |= {'hello', 'world'}
		a.addItems([TaxonSrc('B'), TaxonSrc('C')])
		# Cloned hierarchy
		dst = a.clone(CoreDst())
		self.assertEqual(str(dst), 'A(B(), C())')
		self.assertIn('hello', dst.attrs)
		self.assertIn('world', dst.attrs)

	def testFindOwner(self):
		c = taxonEx('T3')
		b = taxonEx('T2', [c])
		a = taxonEx('T1', [b])
		# Success
		result = c.findOwner('T1')
		self.assertEqual(result, a)
		# Fail with empty result
		result = c.findOwner('T4')
		self.assertIsNone(result)
		with self.assertRaises(RuntimeError) as ex:
			result = c.findOwner('T4', True)
		self.assertEqual(ex.exception.args[0], 'Not found owner with type T4')

	def testFindUpAndDown(self):
		# Сначала считать иерархию
		# packageTest
		# +-folder1
		# | +-folder11
		# | | +-A.wpp
		# | |   +-class A
		# | +-folder12
		# |   +-C.wpp
		# |     +-class C
		# +-folder2
		# | +-folder21
		# |   +-B.wpp
		# |   +-class B
		# | +-folder22
		# +-A.wpp
		#   +-class A
		from Wpp.WppPackage import WppPackage
		rootPath = os.path.join( os.path.split(__file__)[0], 'Wpp', 'tests', 'packageTest' )
		root = WppPackage('packageTest')
		root.read(rootPath)
		root.fullUpdate()
		# try to find package folder12
		listF12 = root.findDown('folder12')
		self.assertEqual(len(listF12), 1)
		self.assertEqual(listF12[0].type, 'Package')
		self.assertEqual(listF12[0].name, 'folder12')
		# try to find class B
		listB = root.findDown('B')
		self.assertEqual(len(listB), 1)
		b = listB[0]
		self.assertEqual(b.type, 'Class')
		self.assertEqual(b.name, 'B')
		# try to find B from itself. must be ok
		res = b.findUp('B', b, b)
		self.assertEqual(res, b)
		# try to find A from B
		with self.assertRaises(ErrorTaxon) as ex:
			res = b.findUp('A', b, b)
		self.assertEqual(ex.exception.args[0], 'Multiply declaration of "A" in [packageTest.A.A, packageTest.folder1.folder11.A.A]')
		# try to find C from B
		c = b.findUp('C', b, b)
		self.assertEqual(c.type, 'Class')
		self.assertEqual(c.name, 'C')

	def testLocationFind(self):
		source = """
func brackets: String
	param s: String
	"(" + s + ")"
func public main
	var r: String = brackets("Hello")
		"""
		module = WppCore.createMemModule(source, 'brackets.fake')
		main = module.dictionary['main'].items[0]
		self.assertEqual(main.type, 'Func')
		self.assertIsNotNone(main.location)
		r = main.getBody().items[0]
		self.assertEqual(r.type, 'Var')
		self.assertIsNotNone(r.location)
		c = r.getValueTaxon()
		self.assertEqual(c.type, 'Call')
		self.assertIsNone(c.location)
		self.assertEqual(c.getLocation(), r.location)
		p = c.getArguments()[0]
		self.assertEqual(p.type, 'Const')
		self.assertEqual(p.getLocation(), r.location)

