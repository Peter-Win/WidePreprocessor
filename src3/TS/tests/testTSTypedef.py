import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSTypedef(unittest.TestCase):
	def testExport(self):
		source = 'typedef public Size = unsigned long'
		tsModule = TSCore.createModuleFromWpp(source, 'export.wpp')
		ctx = OutContextMemoryStream()
		tsModule.exportContext(ctx, style)
		# TypeScript is not maintain unsigned types
		self.assertEqual(str(ctx), 'export type Size = number;')