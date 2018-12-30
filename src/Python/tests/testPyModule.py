import unittest
import os
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyModule(unittest.TestCase):
	def testSimpleExport(self):
		source = """
# First
# Second
# Third
class Simple
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.clone(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext).strip(), '\"\"\"  First\n Second\n Third \"\"\"\nclass Simple:\n\tpass')