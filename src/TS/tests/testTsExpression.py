import unittest
from Wpp.WppCore import WppCore
from TS.TsCore import TsCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTsExpression(unittest.TestCase):
	def testArrayValue(self):
		source = """
var const myList: Array String = ["First", "Second", "Third"]
		"""
		expected = """
export const myList: string[] = ['First', 'Second', 'Third'];
		"""
		srcModule = WppCore.createMemModule(source, 'arrayValue.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testIdExpr(self):
		source = """
class IdExpr
	field myField: int = 256
	method someFunc
		param myParam: String
		var const v1: int = myField
		var const v2: String = myParam
		"""
		expected = """
export class IdExpr {
	private myField: number = 256;
	public someFunc(myParam: string) {
		const v1: number = this.myField;
		const v2: string = myParam;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'IdExpr.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testFieldExpr(self):
		source = """
class FieldTest
	field myField: double
	method useField
		param another: const ref FieldTest
		var const x: double = another.myField
		"""
		expected = """
export class FieldTest {
	private myField: number;
	public useField(another: FieldTest) {
		const x: number = another.myField;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'fieldExpr.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testThisNull(self):
		source = """
class public MyTest
	field value: MyTest = null
	method work
		param value: MyTest
		this.value = value
		"""
		expected = """
export class MyTest {
	private value: MyTest = null;
	public work(value: MyTest) {
		this.value = value;
	}
}
		"""
		srcModule = WppCore.createMemModule(source, 'thisNull.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), WppCore.strPack(expected))

	def testBool(self):
		source = """
var const public myTrue: bool = true
var const public myFalse: bool = false
		"""
		expected = """
export const myTrue: boolean = true;
export const myFalse: boolean = false;
		"""
		srcModule = WppCore.createMemModule(source, 'bool.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))

	def testCallAndNew(self):
		source = """
class A
	method work
func public main
	var const a: A = A()
	a.work()
		"""
		expected = """
class A {
	public work() {
	}
}

export function main() {
	const a: A = new A();
	a.work();
}
		"""
		srcModule = WppCore.createMemModule(source, 'A.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))

	def testBinOp(self):
		source = """
var const public first: int = 2 + 3 * 4
var const public second: int = (2 + 3) * 4
var const public bin: bool = true == first < second
		"""
		expected = """
export const first: number = 2 + 3 * 4;
export const second: number = (2 + 3) * 4;
export const bin: boolean = (true === first) < second;
		"""
		srcModule = WppCore.createMemModule(source, 'A.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))

	def testUnOp(self):
		source = """
var const public a: int = -20
var const public b: int = -a
var const public c: int = ~b
var const public d: bool = !c
var const public e: int = -a * -b
var const public f: int = -(a & b)
		"""
		expected = """
export const a: number = -20;
export const b: number = -a;
export const c: number = ~b;
export const d: boolean = !c;
export const e: number = -a * -b;
export const f: number = -(a & b);
		"""
		srcModule = WppCore.createMemModule(source, 'unOp.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))

	def testTernaryOp(self):
		source = """
var const public a: int = 123
var const public b: int = a < 0 ? -1 : 1
var const public c: int = a < b ? 0 : a + b
var const public d: int = a < b ? 0 : (a + b)
var const public e: int = (a < b ? 0 : a) + b
		"""
		expected = """
export const a: number = 123;
export const b: number = a < 0 ? -1 : 1;
export const c: number = a < b ? 0 : a + b;
export const d: number = a < b ? 0 : a + b;
export const e: number = (a < b ? 0 : a) + b;
		"""
		srcModule = WppCore.createMemModule(source, 'ternaryOp.fake')
		dstModule = srcModule.cloneRoot(TsCore())
		outContext = OutContextMemoryStream()
		dstModule.export(outContext)
		self.assertEqual(str(outContext), dstModule.strPack(expected))
