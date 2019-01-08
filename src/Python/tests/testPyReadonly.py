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
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())