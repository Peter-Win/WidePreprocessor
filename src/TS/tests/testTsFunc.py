import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsFunc(unittest.TestCase):
	def testMethods(self):
		source = """
class Test
	method private hidden: bool
		param instance: Test
	method public static main
		param title: String
		"""
		expected = """
export class Test {
	private hidden(instance: Test): boolean {
	}
	public static main(title: string) {
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'simple.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), expected.strip())