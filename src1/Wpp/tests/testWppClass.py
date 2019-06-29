import unittest
from core.ErrorTaxon import ErrorTaxon
from Wpp.WppClass import WppClass
from Wpp.Context import Context
from Wpp.WppCore import WppCore
from out.OutContextMemory import OutContextMemory
from out.OutContextMemoryStream import OutContextMemoryStream

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
		fileName, n, line = class1._location
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
		self.assertEqual(myClass.getCommentLines(), [' This is comment'])

		outCtx = OutContextMemory()
		myClass.export(outCtx)
		self.assertEqual(str(outCtx), 'class public MyClass\n\t# This is comment')

	def testImplements(self):
		source = """
interface public First
interface public Second
	extends First
interface public Third
class public A
class public B
	extends A
	implements Second Third
		"""
		module = WppCore.createMemModule(source, 'imp.fake')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))

	def testInvalidParent(self):
		source = """
interface public A
class public B
	extends A
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Invalid parent root.A:Interface')
		source = """
class public A
class public B
	implements A
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Invalid interface root.A:Class')

	def testFields(self):
		source = """
class public A
	field counter: unsigned int = 55
		# This is size
	readonly size: unsigned int = 112
		"""
		module = WppCore.createMemModule(source, 'module.fake')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))

	def testUpcast(self):
		source = """
class public A
var public instA: A = null
class public simple B
var public instB: ptr B = null
		"""
		module = WppCore.createMemModule(source, 'module.fake')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), module.strPack(source))
		source = """
class public simple B
var public instB: B = null
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot use null for simple class "B" without pointer')

	def testMethod(self):
		source = """
class A
	method static first
	method const second: int
		param a: A
		param x: double
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'A.memory'))
		a = module.dictionary['A']
		self.assertIn('first', a.dictionary)
		over1 = a.dictionary['first']
		self.assertEqual(over1.name, 'first')
		self.assertIn('static', over1.attrs)

		self.assertIn('second', a.dictionary)
		over2 = a.dictionary['second']
		self.assertEqual(over2.name, 'second')
		self.assertEqual(over2.attrs, {'public'})
		fn2 = over2.items[0]
		self.assertEqual(fn2.name, 'second')
		self.assertIn('const', fn2.attrs)
		self.assertIn('a', fn2.dictionary)
		self.assertIn('x', fn2.dictionary)
		paramA = fn2.getParams()[0]
		self.assertEqual(paramA.name, 'a')
		self.assertEqual(paramA.getLocalType().type, 'TypeName')
		self.assertEqual(paramA.getLocalType().typeRef.target, a)

	def testConstructor(self):
		from Wpp.WppFunc import WppConstructor
		source = """
class public Test
	field fieldA: int
	field fieldB: double = 0
	constructor
		param paramA: int
		param paramB: double
		this.fieldA = paramA
		this.fieldB = paramB
		"""
		module = WppCore.createMemModule(source, 'Test.fake')
		classTest = module.dictionary['Test']
		over = classTest.findConstructor()
		self.assertIsNotNone(over)
		self.assertEqual(over.type, 'Overloads')
		c = over.items[0]
		self.assertEqual(c.type, 'Constructor')
		self.assertEqual(c.name, WppConstructor.key)
		self.assertIn('paramA', c.dictionary)
		self.assertIn('paramB', c.dictionary)
		a = c.dictionary['paramA']
		self.assertEqual(a.type, 'Param')
		self.assertEqual(a.getLocalType().exportString(), 'int')

		outCtx = OutContextMemory()
		classTest.export(outCtx)
		self.assertEqual(str(outCtx), source.strip())

	def testAutoInit(self):
		source = """
class public A
	field a: int
	field b: double
	constructor
		param init a
		param init b = 1.0
		"""
		module = WppCore.createMemModule(source, 'A.fake')
		classA = module.dictionary['A']
		over = classA.findConstructor()
		self.assertIsNotNone(over)
		c = over.items[0]
		a = c.dictionary['a']
		self.assertIn('init', a.attrs)
		self.assertEqual(classA.dictionary['a'], a.fieldRef)
		autoInits = c.getAutoInits()
		self.assertEqual(len(autoInits), 2)

		outCtx = OutContextMemory()
		classA.export(outCtx)
		self.assertEqual(str(outCtx), source.strip())

	def testInvalidNew(self):
		source = """
class A
class B
var public a: A = B()
		"""
		with self.assertRaises(RuntimeError) as cm:
			module = WppCore.createMemModule(source, 'root.fake')
		self.assertEqual(cm.exception.args[0], 'Cannot convert from "B():B" to "A"')

	def testValidEq(self):
		source = """
class A
class B
	extends A
var firstA: A = A()
var firstB: B = B()
var public secondA: A = firstA
var public thirdA: A = firstB
		"""
		module = WppCore.createMemModule(source, 'root.fake')
		outCtx = OutContextMemoryStream()
		module.export(outCtx)
		self.assertEqual(str(outCtx), source.strip())

