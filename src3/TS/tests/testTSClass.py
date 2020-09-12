import unittest
from TS.TSCore import TSCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.style import style

class TestTSClass(unittest.TestCase):
	def testExtends(self):
		source = """
class Top
class Middle
	extends Top
class Bottom
	extends Middle
"""
		expected = """
class Top {
}
class Middle extends Top {
}
class Bottom extends Middle {
}
"""
		module = TSCore.createModuleFromWpp(source, 'extends.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
