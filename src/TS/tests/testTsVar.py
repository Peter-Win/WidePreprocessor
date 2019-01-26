import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsVar(unittest.TestCase):
	def testVarExternal(self):
		""" Variable - member of module """
		source = """
var hidden: bool
var public visible: double = 1.5
		"""
		expected = """
let hidden: boolean;

export let visible: number = 1.5;
		"""
		srcModule = WppCore.createMemModule(source, 'var.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testField(self):
		source = """
class Hello
	field count: unsigned long
	field public value: String = "Hello!"
	field public static inst: Hello
		"""
		expected = """
export class Hello {
	private count: number;
	public value: string = 'Hello!';
	public static inst: Hello;
}
		"""
		srcModule = WppCore.createMemModule(source, 'var.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testParam(self):
		source = """
func public getInfo: String
	param name: String
	param prefix: String = "Hello, "
		"""
		expected = """
export function getInfo(name: string, prefix: string = 'Hello, '): string {
}
		"""
		srcModule = WppCore.createMemModule(source, 'param.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))
