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
	s = 'Hello!'
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

	def testStringStr(self):
		source = """
var s: String = String(15)
		"""
		srcModule = WppCore.createMemModule(source, 'toa.fake')
		s = srcModule.dictionary['s']
		v = s.getValueTaxon()
		self.assertEqual(v.type, 'New')
		c = v.getCaller()
		self.assertEqual(c.type, 'IdExpr')
		wString = c.refs['decl']
		self.assertEqual(wString.name+':'+wString.type, 'String:Class')

		dstModule = srcModule.cloneRoot(PyCore())
		s1 = dstModule.dictionary['s']
		v1 = s1.getValueTaxon()
		self.assertEqual(v1.type, 'New')
		c1 = v1.getCaller()
		self.assertEqual(c1.type, 'IdExpr')
		pString = c1.refs['decl']
		self.assertEqual(pString.name, 'String')

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), 's = str(15)')

