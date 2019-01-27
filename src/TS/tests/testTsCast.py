import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsCast(unittest.TestCase):
	def testCast(self):
		source = """
class A
	field name: String
	constructor
		param init name
	cast const: String
		name
func public main
	var const a: A = A("Hello!")
	var const s: String = String(a)
		"""
		expected = """
class A {
	private name: string;
	public constructor(name: string) {
		this.name = name;
	}
	public toString(): string {
		return this.name;
	}
}
export function main() {
	const a: A = new A('Hello!');
	const s: string = String(a);
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

