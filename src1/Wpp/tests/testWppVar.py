import unittest
from Wpp.WppVar import WppVar
from Wpp.Context import Context
from Wpp.WppCore import WppCore
from out.OutContextMemory import OutContextMemory
from out.OutContextMemoryStream import OutContextMemoryStream

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
		self.assertEqual(localType.typeRef.target.type, classFirst.type)
		self.assertEqual(localType.typeRef.target, classFirst)

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
		module = WppCore.createMemModule(source, 'First.memory')
		classPoint = module.dictionary['Point']
		classRect = module.dictionary['Rect']
		self.assertIn('a', classRect.dictionary)
		self.assertIn('b', classRect.dictionary)

		a = classRect.dictionary['a']
		self.assertEqual(a.type, 'Field')
		self.assertEqual(a.name, 'a')
		self.assertEqual(a.getLocalType().typeRef.target, classPoint)
		self.assertEqual(a.getAccessLevel(), 'public')

		b = classRect.dictionary['b']
		self.assertEqual(b.name, 'b')
		self.assertEqual(b.getAccessLevel(), 'private')
		outContext = OutContextMemory()
		b.export(outContext)
		self.assertEqual(str(outContext), 'field b: Point\n\t# this is b')


	def testInitValue(self):
		source = """
class A
	field counter: int = -1
		"""
		module = WppCore.createMemModule(source, 'First.memory')
		classA = module.dictionary['A']
		counter = classA.dictionary['counter']
		self.assertEqual(counter.getLocalType().exportString(), 'int')
		v = counter.getValueTaxon()
		self.assertIsNotNone(v)
		self.assertEqual(v.exportString(), '-1')


	def testReadonly(self):
		source = """
class public Atom
	readonly N: int
	readonly mass: double
	constructor
		param init N
		param init mass
func public main
	var H: Atom = Atom(1, 1.008)
	var O: Atom = Atom(8, 15.999)
	var waterMass: double = H.mass * 2 + O.mass
		"""
		module = WppCore.createMemModule(source, 'readonly.fake')
		Atom = module.dictionary['Atom']
		mass = Atom.dictionary['mass']
		self.assertEqual(mass.type, 'Readonly')
		self.assertIn('public', mass.attrs)
		self.assertEqual(mass.getLocalType().exportString(), 'double')
		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
