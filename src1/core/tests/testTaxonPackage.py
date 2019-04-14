import unittest
from Taxon import Taxon
from core.TaxonPackage import TaxonPackage
from core.ErrorTaxon import ErrorTaxon
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTaxonPackage(unittest.TestCase):
	def testFind(self):
		common = TaxonPackage('common')
		left = common.addItem(TaxonPackage('left'))
		middle = common.addItem(TaxonPackage('middle'))
		right = common.addItem(TaxonPackage('right'))
		class MyModule(Taxon):
			type = 'Module'
			def findDown(self, params):
				return self._findDownRecursive(params)
		class MyClass(Taxon):
			type = 'Class'
		def pair(owner, name):
			module = owner.addItem(MyModule(name))
			return module, module.addItem(MyClass(name))
		moduleA, classA = pair(left, 'A')
		moduleB, classB = pair(left, 'B')
		moduleM, classM = pair(middle, 'M')
		moduleR, classR = pair(right, 'R')
		moduleB1, classB1 = pair(right, 'B')
		self.assertEqual(classM.findUpEx('A'), classA)
		self.assertEqual(classA.findUpEx('B'), classB)
		self.assertEqual(classR.findUpEx('B'), classB1)
		with self.assertRaises(ErrorTaxon) as cm:
			classM.findUpEx('B')
		self.assertEqual(str(cm.exception), '*Error* Multiply declaration of "B" in [common.left.B.B, common.right.B.B]')

	def testExport(self):
		class MyPackage(TaxonPackage):
			def onNewFolder(self, ctx):
				ctx.writeln('>'+self.getPath())
		class MyTaxon(Taxon):
			def export(self, outContext):
				outContext.writeln(' -'+self.name)
		common = MyPackage('common')
		first = common.addItem(MyPackage('first'))
		first.addItems([MyTaxon('Point'), MyTaxon('Rect')])
		second = common.addItem(MyPackage('second'))
		second.addItems([MyTaxon('Circle'), MyTaxon('Ellipse')])
		ctx = OutContextMemoryStream()
		common.export(ctx)
		result = """>common
>common.first
 -Point
 -Rect
>common.second
 -Circle
 -Ellipse"""
		self.assertEqual(str(ctx), result)
