import unittest
from Wpp.WppCore import WppCore
from Wpp.WppModule import WppModule
from Wpp.Context import Context
from out.OutContextMemoryStream import OutContextMemoryStream

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