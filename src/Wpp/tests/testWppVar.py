import unittest
from Wpp.WppVar import WppVar
from Wpp.Context import Context
from Wpp.WppCore import WppCore
from out.OutContextMemory import OutContextMemory

class TestWppVar(unittest.TestCase):
	def testVarInModule(self):
		source = """
class public First
var private myVar: First
	# This is my variable
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'First.memory'))
		self.assertIn('First', module.dictionary)
		self.assertIn('myVar', module.dictionary)
		classFirst = module.dictionary['First']
		myVar = module.dictionary['myVar']
		self.assertEqual(myVar.name, 'myVar')
		self.assertEqual(myVar.type, 'Var')
		localType = myVar.getLocalType()
		self.assertEqual(localType.type, 'TypeName')
		self.assertEqual(localType.getTypeTaxon(), classFirst)

		outContext = OutContextMemory()
		myVar.export(outContext)
		self.assertEqual(str(outContext), 'var private myVar: First\n\t# This is my variable')

	def testFieldInClass(self):
		source = """
class public simple Point
class public Rect
	field public a: Point
		# this is a
	field b: Point
		# this is b
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'First.memory'))
		classPoint = module.dictionary['Point']
		classRect = module.dictionary['Rect']
		self.assertIn('a', classRect.dictionary)
		self.assertIn('b', classRect.dictionary)

		a = classRect.dictionary['a']
		self.assertEqual(a.type, 'Field')
		self.assertEqual(a.name, 'a')
		self.assertEqual(a.getLocalType().getTypeTaxon(), classPoint)
		self.assertEqual(a.getAccessLevel(), 'public')

		b = classRect.dictionary['b']
		self.assertEqual(b.name, 'b')
		self.assertEqual(b.getAccessLevel(), 'private')
		outContext = OutContextMemory()
		b.export(outContext)
		self.assertEqual(str(outContext), 'field private b: Point\n\t# this is b')


	def testInitValue(self):
		source = """
class A
	field counter: int = -1
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'First.memory'))
		classA = module.dictionary['A']
		counter = classA.dictionary['counter']
		self.assertEqual(counter.getLocalType().exportString(), 'int')
		v = counter.getValueTaxon()
		self.assertIsNotNone(v)
		self.assertEqual(v.exportString(), '-1')
