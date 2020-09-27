import unittest
from TS.TSCore import TSCore
from out.OutContextMemoryStream import OutContextMemoryStream
from TS.style import style

class TestTSClass(unittest.TestCase):
	def testSimpleField(self):
		source = """
class Value
	field public value: double = 1.0
	method setValue
		param v: double
		value = v
"""
		expected = """
class Value {
    public value = 1.0;
    setValue(v: number): void {
        this.value = v;
    }
}
"""
		module = TSCore.createModuleFromWpp(source, 'simple.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testStaticField(self):
		source = """
class Value
	field public value: double = 1.0
	field private static epsilon: double = 0.001
	method is0: bool
		return value < epsilon
"""
		expected = """
class Value {
    public value = 1.0;
    private static epsilon = 0.001;
    is0(): boolean {
        return this.value < Value.epsilon;
    }
}
"""
		module = TSCore.createModuleFromWpp(source, 'static.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
