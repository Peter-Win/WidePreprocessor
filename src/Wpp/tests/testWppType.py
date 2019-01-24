import unittest
from Wpp.WppType import WppType, splitComma
from Wpp.Context import Context
from Wpp.WppCore import WppCore

class TestWppType(unittest.TestCase):
	def testTypeName(self):
		source = """class public A"""
		core = WppCore()
		ctx = Context.createFromMemory(source, 'A.memory')
		module = core.createRootModule(ctx)
		classA = module.dictionary['A']
		self.assertEqual(classA.type, 'Class')
		# Создать таксон типа из строкового описания. Со ссылкой на класс внутри модуля
		typeTaxon = WppType.create('const ref A', ctx)
		self.assertEqual(typeTaxon.type, 'TypeName')
		# Хотя это бессмысленно, но добавить тип в модуль.Чтобы в процессе update была найдена ссылка на класс A
		module.addItem(typeTaxon)
		typeTaxon.fullUpdate()
		declA = typeTaxon.getTypeTaxon()
		self.assertEqual(classA, declA)

	def testSplitComma(self):
		groups = splitComma('A B C'.split())
		self.assertEqual(len(groups), 1)
		self.assertEqual(groups[0], ['A', 'B', 'C'])

		groups = splitComma('A B, C'.split())
		self.assertEqual(len(groups), 2)
		self.assertEqual(groups[0], ['A', 'B'])
		self.assertEqual(groups[1], ['C'])

		groups = splitComma('A B , C'.split())
		self.assertEqual(len(groups), 2)
		self.assertEqual(groups[0], ['A', 'B'])
		self.assertEqual(groups[1], ['C'])

		groups = splitComma('A, B , C'.split())
		self.assertEqual(len(groups), 3)
		self.assertEqual(groups[0], ['A'])
		self.assertEqual(groups[1], ['B'])
		self.assertEqual(groups[2], ['C'])

	def testMap(self):
		ctx = Context.createFromMemory('', 'A.memory')
		source = 'const Map String, double'
		t = WppType.create(source, ctx)
		self.assertEqual(t.type, 'TypeMap')
		self.assertIn('const', t.attrs)
		self.assertEqual(t.getKeyType().type, 'TypeName')
		self.assertEqual(t.getValueType().type, 'TypeName')

	def testPath(self):
		source = """
class public Point
	typedef Value: double
	field public x: Value
	field public y: Value

class public Rect
	typedef Value: Point.Value
		"""
		module = WppCore.createMemModule(source, 'Rect.fake')
