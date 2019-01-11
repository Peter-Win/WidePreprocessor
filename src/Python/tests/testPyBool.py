import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyBool(unittest.TestCase):
	def testBool(self):
		source = """
func public main
	var no: bool
	var yes: bool = true
	var res: bool = no == true
		"""
		expected = """
def main():
	no = False
	yes = True
	res = no == True
		"""
		srcModule = WppCore.createMemModule(source, 'bool.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())