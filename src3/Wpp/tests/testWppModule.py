import unittest
from Wpp.WppCore import WppCore
from Wpp.WppModule import WppModule
from Wpp.Context import Context
from out.OutContextMemoryStream import OutContextMemoryStream
from core.ErrorTaxon import ErrorTaxon

class TestWppModule(unittest.TestCase):
	def testCreateInstance(self):
		core = WppCore.createInstance()
		self.assertEqual(core.getDebugStr(), 'WppCore')
		module = core.creator('module')()
		self.assertEqual(module.type, 'module')

	def testCreateMemModule(self):
		source = ''
		module = WppCore.createMemModule(source, 'myModule.mem')
		self.assertEqual(module.type, 'module')

	def testComments(self):
		source = """
# Hello!
# Module description
"""
		module = WppCore.createMemModule(source, 'myModule.mem')
		ctx = OutContextMemoryStream()
		module.export(ctx)
		self.assertEqual(str(ctx), source.strip())

	def testDuplicate(self):
		source = """
var public abcd: double = 123
func public abcd: double
	return 123
"""
		with self.assertRaises(ErrorTaxon) as cm:
			module = WppCore.createMemModule(source, 'dup.mem')
		self.assertEqual(cm.exception.args[0], 'Duplicate identifier "abcd"')

