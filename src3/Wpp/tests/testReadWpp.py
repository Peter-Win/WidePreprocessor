import unittest
from Wpp.readWpp import readWpp
from Wpp.Context import Context
from Wpp.WppTaxon import WppTaxon
from Taxon import Taxon
from core.ErrorTaxon import ErrorTaxon

class DemoTaxon(Taxon, WppTaxon):
	def getDebugStr(self):
		return '%s %s' % (self.type, self.name)
	def readHead(self, context):
		words = context.currentLine.split()
		self.name = words[1]

class Core(DemoTaxon):
	type = 'core'
	validSubTaxons = ('module')
	def __init__(self):
		super().__init__()
		self.core = self
		self.taxonMap = {'module': Module, 'class': Class}
	def getDebugStr(self):
		return 'Core'

class Module(DemoTaxon):
	type = 'module'
	validSubTaxons = ('module', 'class')
	def checkName(self, name):
		return ''

class Class(DemoTaxon):
	type = 'class'
	validSubTaxons = ()
	def checkName(self, name):
		return ''


class TestReadWpp(unittest.TestCase):
	def testMain(self):
		lines = """
module Left
	class A1
	class A2
module Middle
module Right
	module SubRight
		class C1
		"""
		context = Context.createFromMemory(lines, 'main')
		core = Core()
		readWpp(context, core)
		self.assertEqual(len(core.items), 3)
		left, middle, right = core.items
		self.assertEqual(left.type, 'module')
		self.assertEqual(left.name, 'Left')
		self.assertEqual(len(left.items), 2)
		self.assertEqual(left.items[0].type, 'class')
		self.assertEqual(left.items[0].name, 'A1')
		self.assertEqual(left.items[1].type, 'class')
		self.assertEqual(left.items[1].name, 'A2')

		self.assertEqual(middle.type, 'module')
		self.assertEqual(middle.name, 'Middle')
		self.assertEqual(len(middle.items), 0)

		self.assertEqual(right.type, 'module')
		self.assertEqual(right.name, 'Right')
		self.assertEqual(len(right.items), 1)
		subRight = right.items[0]
		self.assertEqual(subRight.type, 'module')
		self.assertEqual(subRight.name, 'SubRight')
		self.assertEqual(len(subRight.items), 1)
		self.assertEqual(subRight.items[0].type, 'class')
		self.assertEqual(subRight.items[0].name, 'C1')

	def testOffsetError(self):
		lines = """
module A
		class B
		"""
		context = Context.createFromMemory(lines, 'main')
		core = Core()
		with self.assertRaises(ErrorTaxon) as cm:
			readWpp(context, core)
		self.assertEqual(cm.exception.args[0], 'Invalid offset')
