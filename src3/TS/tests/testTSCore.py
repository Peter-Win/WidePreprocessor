import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSCore(unittest.TestCase):
	def testReservedWords(self):
		core = TSCore.createInstance()
		self.assertEqual(core.getSafeName('myName'), 'myName')
		self.assertEqual(core.getSafeName('class'), 'class_')
		self.assertEqual(core.getSafeName('from'), 'from_')

	def testAlias(self):
		"""Alias of core type"""
		source = "var const public firstByte: byte = 15"
		tsModule = TSCore.createModuleFromWpp(source, 'alias.wpp')
		ctx = OutContextMemoryStream()
		tsModule.exportContext(ctx, style)
		# transform byte into number
		self.assertEqual(str(ctx), 'export const firstByte: number = 15;')