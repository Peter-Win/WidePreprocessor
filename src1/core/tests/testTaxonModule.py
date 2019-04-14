import unittest
from Taxon import Taxon
from core.TaxonModule import TaxonModule
from core.TaxonPackage import TaxonPackage
from core.ErrorTaxon import ErrorTaxon
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTaxonModule(unittest.TestCase):
	def testFind(self):
		root = TaxonPackage('root')
		left = root.addNamedItem(TaxonPackage('left'))
		middle = root.addNamedItem(TaxonPackage('middle'))
		right = root.addNamedItem(TaxonPackage('right'))
		class MyClass(Taxon):
			pass
		def pair(owner, name):
			module = owner.addNamedItem(TaxonModule(name))
			cls = module.addNamedItem(MyClass(name))
			cls.attrs.add('public')
			return module, cls
		def keys(dictTaxon):
			leftKeys = list(dictTaxon.dictionary.keys())
			leftKeys.sort()
			return ', '.join(leftKeys)
		moduleA, classA = pair(left, 'A')
		moduleA.addNamedItem(MyClass('Hidden'))
		moduleB, classB = pair(left, 'B')
		moduleM, classM = pair(middle, 'M')
		moduleZ, classZ = pair(right, 'Z')
		moduleB1, classB1 = pair(right, 'B')
		self.assertEqual(classB.findUp(classB, {'name': 'B', 'isModule': True}), moduleB) # Свой модуль
		self.assertEqual(classB.findUpEx('left'), left) # Свой пакет
		self.assertEqual(keys(left), 'A, B')
		self.assertEqual(classB.findUp(classB, {'name': 'A', 'isModule': True}), moduleA) # Соседний модуль в своем пакете
		self.assertEqual(keys(moduleA), 'A, Hidden')
		self.assertEqual(classB.findUpEx('A'), classA) # Класс в модуле своего пакета
		with self.assertRaises(ErrorTaxon) as cm: # Нельзя найти элемент модуля, который не public
			classB.findUpEx('Hidden')
		self.assertEqual(str(cm.exception), '*Error* Name "Hidden" is not defined')
		self.assertEqual(classA.findUpEx('Hidden').name, 'Hidden') # Из класса A можно найти Hidden, т.к. они в одном модуле
		self.assertEqual(classA.findUpEx('B'), classB) # Из A можно найти класс В, т.к они в одном пакете
		with self.assertRaises(ErrorTaxon) as cm: # для класса из пакета middle не получится найти B, т.к. он есть в left и right
			classM.findUpEx('B')
		self.assertEqual(str(cm.exception), '*Error* Multiply declaration of "B" in [root.left.B.B, root.right.B.B]')
		self.assertEqual(classZ.findUpEx('B'), classB1) # Класс Z находит B в своем пакете right
		self.assertEqual(classZ.findUpEx('A'), classA) # Находим класс A, т.к. он имеет уникальное имя
		self.assertEqual(classZ.findUp(classZ, {'name': 'A', 'isModule': True}), moduleA) # Поиск модуля в другом пакете

	def testExport(self):
		class MyModule(TaxonModule):
			extension = 'my'
			def exportComment(self, outContext):
				for line in self.getCommentLines():
					outContext.writeln('# '+line)
		class MyClass(Taxon):
			def export(self, outContext):
				outContext.writeln('-'+self.name)
		moduleA = MyModule('A')
		moduleA.addComment('Module A')
		moduleA.addNamedItem(MyClass('Hello'))
		moduleA.addNamedItem(MyClass('World'))
		ctx = OutContextMemoryStream()
		moduleA.export(ctx)
		result = '# Module A\n-Hello\n-World'
		self.assertEqual(str(ctx), result)

	def testFindModule(self):
		package = TaxonPackage('package')
		module = package.addItem(TaxonModule('module'))
		first = module.addItem(Taxon('first'))
		second = first.addItem(Taxon('second'))
		third = second.addItem(Taxon('third'))
		self.assertEqual(third.findModule(), module)
