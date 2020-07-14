import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSVar(unittest.TestCase):
	def testComment(self):
		source = """
var const public bufferSize: size_t = 256
	# This is comment.
	# Second line...
"""
		expected = """
// This is comment.
// Second line...
export const bufferSize: number = 256;
"""
		tsModule = TSCore.createModuleFromWpp(source, 'comment.wpp')
		ctx = OutContextMemoryStream()
		tsModule.exportContext(ctx, style)
		self.assertEqual(str(ctx), expected.strip())