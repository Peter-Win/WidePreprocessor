import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyString(unittest.TestCase):
	def testString(self):
		source = """
func public main
	var s: String = "Hello!"
	var n: unsigned long = s.length
		"""
		expected = """
def main():
	s = "Hello!"
	n = len(s)
		"""
		srcModule = WppCore.createMemModule(source, 'string.fake')
		dstModule = srcModule.cloneRoot(PyCore())
		mainOver = dstModule.dictionary['main']
		mainFunc = mainOver.items[0]
		cmd2 = mainFunc.getBody().items[1]
		self.assertEqual(cmd2.type, 'Var')
		expr = cmd2.getValueTaxon()
		self.assertEqual(expr.type, 'Call')
		lenId = expr.getCaller()
		self.assertEqual(lenId.type, 'IdExpr')
		self.assertEqual(lenId.id, 'len')
		lenDecl = lenId.getDeclaration()
		self.assertEqual(lenDecl.type, 'Overloads')
		self.assertEqual(lenDecl.name, 'len')

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())