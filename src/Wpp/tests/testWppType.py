import unittest
from Wpp.WppType import WppType
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