import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsMath(unittest.TestCase):
	def testMath(self):
		source = """
func public main
	var const a: double = Math.sin(Math.PI * 0.3)
	var const b: double = Math.min(a, 1)
		"""
		expected = """
export function main() {
	const a: number = Math.sin(Math.PI * 0.3);
	const b: number = Math.min(a, 1);
}
		"""
		srcModule = WppCore.createMemModule(source, 'math.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testAngles(self):
		source = """
func public main
	var const deg: double = Math.degrees(Math.PI / 2)
	var const rad: double = Math.radians(270)
	var const rad2: double = Math.radians(deg + 15)
		"""
		expected = """
export function main() {
	const deg: number = Math.PI / 2 * 57.29577951308232;
	const rad: number = 4.71238898038469;
	const rad2: number = (deg + 15) * 0.017453292519943295;
}
		"""
		srcModule = WppCore.createMemModule(source, 'angles.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))
