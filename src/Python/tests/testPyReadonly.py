import unittest
from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestPyReadonly(unittest.TestCase):
	def testReadonly(self):
		source = """
class public Atom
	readonly mass: double
	constructor
		param init mass

func public main
	var H: Atom = Atom(1.008)
	var O: Atom = Atom(15.999)
	var waterMass: double = H.mass * 2 + O.mass
		"""
		expected = """
class Atom:
	__slots__ = ('_mass')
	@property
	def mass(self):
		return self._mass
	def __init__(self, mass):
		self._mass = mass

def main():
	H = Atom(1.008)
	O = Atom(15.999)
	waterMass = H.mass * 2 + O.mass
		"""
		srcModule = WppCore.createMemModule(source, 'readonly.fake')
		dstModule = srcModule.cloneRoot(PyCore())

		classAtom = dstModule.dictionary['Atom']
		self.assertEqual(classAtom.type, 'Class')
		conOver = classAtom.findConstructor()
		self.assertEqual(conOver.type, 'Overloads')
		con = conOver.items[0]
		self.assertEqual(con.type, 'Constructor')
		cmd = con.getBody().items[0]
		self.assertEqual(cmd.type, 'BinOp')
		self.assertEqual(cmd.opCode, '=')
		pt = cmd.getLeft()
		self.assertEqual(pt.type, 'BinOp')
		self.assertEqual(pt.opCode, '.')
		field = pt.getRight()
		self.assertEqual(field.type, 'FieldExpr')
		self.assertIsNotNone(field.findOwner('Constructor'))

		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())