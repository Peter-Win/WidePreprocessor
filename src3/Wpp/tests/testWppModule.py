import unittest
from Wpp.WppCore import WppCore
from Wpp.WppModule import WppModule
from Wpp.Context import Context

class TestWppModule(unittest.TestCase):
	def testCreateInstance(self):
		core = WppCore.createInstance()
		self.assertEqual(core.getDebugStr(), 'WppCore')
		module = core.creator('module')()
		self.assertEqual(module.type, 'module')

	@unittest.skip('wait for something internal module construction')
	def testReadModule(self):
		core = WppCore.createInstance()
		module = core.addRoot(WppModule('MyModule'))
		source = ''
		context = Context.createFromMemory(source, 'MyModule.memory')
		module.read(context)

	def testCreateMemModule(self):
		source = ''
		module = WppCore.createMemModule(source, 'myModule.mem')
		self.assertEqual(module.type, 'module')
