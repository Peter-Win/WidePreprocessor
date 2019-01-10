import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyArray(unittest.TestCase):
	def testArrayInit(self):
		source = """
func public main
	var vec: Array float = [1.11, 2.22, 3.33]
		"""
		expected = """
def main():
	vec = [1.11, 2.22, 3.33]
		"""
		srcModule = WppCore.createMemModule(source, 'arrayInit.fake')
		dstModule = srcModule.cloneRoot(PyCore())

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())