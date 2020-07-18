import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSFunc(unittest.TestCase):
	def testShortForm(self):
		source = """
func public shortFunc: double
	param singleParam: double
	return singleParam
"""
		expected = 'export const shortFunc = (singleParam: number): number => singleParam;'
		module = TSCore.createModuleFromWpp(source, 'shortForm.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), expected)


