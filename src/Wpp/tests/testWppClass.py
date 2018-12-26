import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppClass import WppClass
from Wpp.Context import Context
from Wpp.WppCore import WppCore
from out.OutContextMemory import OutContextMemory

class TestWppClass(unittest.TestCase):

	def testReadHead(self):
		src = """
		class First
		class simple abstract Second
		class
		"""
		ctx = Context.createFromMemory(src, 'testClass')

		ctx.readLine() # class First
		class1 = WppClass()
		class1.readHead(ctx)
		self.assertEqual(class1.type, 'Class')
		self.assertEqual(class1.name, 'First')
		fileName, n, line = class1.location
		self.assertEqual(fileName, 'testClass')
		self.assertEqual(n, 2)
		self.assertEqual(line, '\t\tclass First')

		ctx.readLine() # class simple abstract Second
		class2 = WppClass()
		class2.readHead(ctx)
		self.assertEqual(class2.name, 'Second')
		self.assertIn('simple', class2.attrs)
		self.assertIn('abstract', class2.attrs)

		ctx.readLine() # class
		class3 = WppClass()
		with self.assertRaises(ErrorTaxon) as ex:
			class3.readHead(ctx)
		msg = ex.exception.args[0]
		self.assertEqual(msg, 'Required class name')
		fileName, n, line = ex.exception.args[1]
		self.assertEqual(n, 4)

	def testExtends(self):
		source = """
class public A
class public B
	extends A
class public C
	extends B
		"""
		ctx = Context.createFromMemory(source, 'textExt.memory')
		core = WppCore()
		module = core.createRootModule(ctx)
		self.assertEqual(module.type, 'Module')
		self.assertEqual(module.name, 'textExt')
		self.assertIn('A', module.dictionary)
		self.assertIn('B', module.dictionary)
		self.assertIn('C', module.dictionary)
		a = module.dictionary['A']
		b = module.dictionary['B']
		c = module.dictionary['C']
		self.assertEqual(b.getParent(), a)

		outCtx = OutContextMemory()
		b.export(outCtx)
		text = '\n'.join(outCtx.lines)
		self.assertEqual(text, 'class public B\n\textends A')

		outCtx = OutContextMemory()
		c.export(outCtx)
		text = '\n'.join(outCtx.lines)
		self.assertEqual(text, 'class public C\n\textends B')

	def testAttributes(self):
		core = WppCore()
		# Error - Incompatible attributes used
		ctx = Context.createFromMemory('class public private A', 'A.memory')
		with self.assertRaises(ErrorTaxon) as ex:
			module = core.createRootModule(ctx)
		ctx = Context.createFromMemory('class static abstract B', 'B.memory')
		with self.assertRaises(ErrorTaxon) as ex:
			module = core.createRootModule(ctx)
		ctx = Context.createFromMemory('class protected C', 'C.memory')
		with self.assertRaises(ErrorTaxon) as ex:
			module = core.createRootModule(ctx)
		ctx = Context.createFromMemory('class static D', 'D.memory')
		module = core.createRootModule(ctx)
		self.assertIn('D', module.dictionary)
		d = module.dictionary['D']
		# Квалификатор доступа должен автоматически установиться в public
		self.assertEqual(d.getAccessLevel(), 'public')

	def testComments(self):
		source = """
class public MyClass
	# This is comment
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'MyClass.memory'))
		myClass = module.dictionary['MyClass']
		self.assertEqual(myClass.getComment(), ' This is comment')

		outCtx = OutContextMemory()
		myClass.export(outCtx)
		self.assertEqual(str(outCtx), 'class public MyClass\n\t# This is comment')
