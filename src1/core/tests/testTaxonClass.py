import unittest
from Taxon import Taxon
from core.TaxonClass import TaxonClass
from core.TaxonInterface import TaxonInterface
from core.TaxonModule import TaxonModule
from core.TaxonPackage import TaxonPackage
from core.ErrorTaxon import ErrorTaxon
from out.OutContextMemoryStream import OutContextMemoryStream
from core.Ref import Ref
from core.TaxonImportBlock import TaxonImportBlock

class TestTaxonClass(unittest.TestCase):
	def testParent(self):
		root = TaxonPackage('root')
		moduleA = root.addNamedItem(TaxonModule('A'))
		classA = moduleA.addNamedItem(TaxonClass('A'))
		classA.attrs.add('public')
		moduleB = root.addNamedItem(TaxonModule('B'))
		classB = moduleB.addNamedItem(TaxonClass('B'))
		classB.parent = Ref('A')
		root.fullUpdate()
		self.assertEqual(classB.getParent(), classA)

	def testFind(self):
		class Field(Taxon):
			def export(self, outContext):
				outContext.writeln('@' + self.name)
		class MyModule(TaxonModule):
			extension = 'my'
			def exportComment(self, ctx):
				pass
		class MyClass(TaxonClass):
			def export(self, ctx):
				ctx.writeln('class %s' % (self.name,))
				ctx.push()
				if self.getParent():
					ctx.writeln('extends %s' % (self.getParent().name,))
				for m in self.getMembers():
					m.export(ctx)
				ctx.pop()
		root = TaxonPackage('root')
		moduleA = root.addNamedItem(MyModule('A'))
		classA = moduleA.addNamedItem(MyClass('A'))
		classA.attrs.add('public')
		txName = classA.addNamedItem(Field('name'))
		moduleB = root.addNamedItem(MyModule('B'))
		moduleB.extension = 'wpp'
		classB = moduleB.addNamedItem(MyClass('B'))
		classB.attrs.add('public')
		classB.parent = Ref('A')
		txBlock = classB.addNamedItem(Field('block'))
		root.fullUpdate()

		ctx = OutContextMemoryStream()
		root.export(ctx)
		text = """
class A
	@name
class B
	extends A
	@block
		"""
		self.assertEqual(str(ctx), Taxon.strPack(text))
		# Необходимо иметь возможность найти поля в родительских классах
		self.assertEqual(txBlock.findUpPath('name'), txName)

	def testImplements(self):
		class MyMember(Taxon):
			pass

		module = TaxonModule('Module')
		iFar = module.addNamedItem(TaxonInterface('IFar'))
		txFar = iFar.addNamedItem(MyMember('far'))
		txMulti1 = iFar.addNamedItem(MyMember('multi'))
		iNear = module.addNamedItem(TaxonInterface('INear'))
		iNear.parent = Ref('IFar')
		txNear = iNear.addNamedItem(MyMember('near'))
		iSecond = module.addNamedItem(TaxonInterface('ISecond'))
		txSecond = iSecond.addNamedItem(MyMember('second'))
		txMulti2 = iSecond.addNamedItem(MyMember('multi'))
		classA = module.addNamedItem(TaxonClass('A'))
		classA.implements = [Ref('INear'), Ref('ISecond')]
		txBlock = classA.addNamedItem(MyMember('block'))
		module.fullUpdate()
		self.assertEqual(txBlock.findUpPath('ISecond'), iSecond)
		self.assertEqual(txBlock.findUpPath('second'), txSecond)
		self.assertEqual(txBlock.findUpPath('far'), txFar)
		with self.assertRaises(RuntimeError) as cm:
			txBlock.findUpPath('multi')
		self.assertEqual(str(cm.exception), '*Error* Multiple definition of "multi" in [Module.IFar.multi, Module.ISecond.multi]')

	def testIsReadyFull(self):
		""" Три класса и интерфейс A<-B<-C=>D. Порядок загрузки C, A, D, B """
		module = TaxonModule('module')
		classA = module.addNamedItem(TaxonClass('A'))
		classB = module.addNamedItem(TaxonClass('B'))
		classB.parent = Ref('A')
		classC = module.addNamedItem(TaxonClass('C'))
		classC.parent = Ref('B')
		intD = module.addNamedItem(TaxonInterface('D'))
		classC.implements.append(Ref('D'))
		self.assertTrue(classA.isReady()) # True, because A have no parent
		self.assertTrue(classA.isReadyFull())
		self.assertFalse(classB.isReady())	# False, because not init ref to parent A
		self.assertFalse(classB.isReadyFull())
		self.assertFalse(classC.isReady())
		self.assertTrue(intD.isReady()) # True, because D have no parent
		classC.update() # Не fullUpdate, т.к. запустится задача, которая будет ждать готовность класса, но она не выполнится
		self.assertTrue(classC.isReady()) # Must init refs to B and D
		self.assertFalse(classB.isReady())
		self.assertFalse(classC.isReadyFull()) # But B is not ready => C is not ready full
		classB.update()
		self.assertTrue(classB.isReady())
		self.assertTrue(classC.isReadyFull()) # All classes are ready

	def testImport(self):
		class MyPackage(TaxonPackage):
			pass
		class MyImportBlock(TaxonImportBlock):
			def export(self, ctx):
				d = self.groupByModules()
				ilist = []
				for module, taxons in d.items():
					moduleInfo = module.getImportInfo(self.owner)
					names = [t.name for t in taxons]
					names.sort()
					ilist.append('import {%s} from %s' % (', '.join(names), moduleInfo['path']))
				ilist.sort()
				for s in ilist:
					ctx.writeln(s)
		class MyModule(TaxonModule):
			extension = 'ts'
			def __init__(self, name = ''):
				super().__init__(name)
				self.importBlock = MyImportBlock(self)
			def exportComment(self, ctx):
				ctx.writeln('// Module ' + self.name + '.' + self.extension)
			def getImportInfo(self, sourceModule):
				return {'path': self.getPath()}

		class MyClass(TaxonClass):
			def export(self, ctx):
				s = 'public class ' + self.getName(self)
				if self.parent:
					s += ' extends ' + self.parent.target.getName(self)
				if len(self.implements):
					names = [i.target.getName(self) for i in self.implements]
					s += ' implements ' + ', '.join(names)
				ctx.writeln(s + ' {}')
			def onUpdate(self):
				super().onUpdate()
				self.addImport(self.getParent())
				for i in self.implements:
					self.addImport(i.target)
		class MyInterface(TaxonInterface):
			def __init__(self, name = ''):
				super().__init__(name)
				self.attrs.add('public')
			def export(self, ctx):
				s = 'public interface ' + self.name
				if self.getParent():
					s += ' extends ' + self.getParent().name
				ctx.writeln(s + ' {}')
			def onUpdate(self):
				super().onUpdate()
				self.addImport(self.getParent())
		root = MyPackage('root')
		moduleA = root.addNamedItem(MyModule('A'))
		moduleB = root.addNamedItem(MyModule('B'))
		moduleC = root.addNamedItem(MyModule('C'))
		classA = moduleA.addNamedItem(MyClass('A'))
		classA.attrs.add('public')
		intAx = moduleA.addNamedItem(MyInterface('Ax'))
		intC0 = moduleC.addNamedItem(MyInterface('C0'))
		intCx = moduleC.addNamedItem(MyInterface('Cx'))
		intCx.parent = Ref('C0') # Здесь не произойдет добавление импорта, т.к. парент в этом же модуле
		classB = moduleB.addNamedItem(MyClass('B'))
		classB.parent = Ref('A')
		classB.implements.append(Ref('Ax'))
		classB.implements.append(Ref('Cx'))
		intAx.parent = Ref('C0')
		root.fullUpdate()
		self.assertTrue(classB.isReadyFull())
		self.assertTrue(classA.isReadyFull())
		ctx = OutContextMemoryStream()
		root.export(ctx)
		src = """
// Module A.ts
import {C0} from root.C
public class A {}
public interface Ax extends C0 {}
// Module B.ts
import {A, Ax} from root.A
import {Cx} from root.C
public class B extends A implements Ax, Cx {}
// Module C.ts
public interface C0 {}
public interface Cx extends C0 {}
		"""
		self.assertEqual(str(ctx), Taxon.strPack(src))
