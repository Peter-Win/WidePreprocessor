import unittest
from TS.TSCore import TSCore
from TS.style import style
from out.OutContextMemoryStream import OutContextMemoryStream

class TestTSSuper(unittest.TestCase):
	def testConstructor(self):
		source = """
class First
	field primary: int
	constructor
		autoinit primary
class Second
	extends First
	field secondary: double
	constructor
		param primary: int
		autoinit secondary
		super(primary)
"""
		expected = """
class First {
    private primary: number;
    constructor(primary: number) {
        this.primary = primary;
    }
}
class Second extends First {
    private secondary: number;
    constructor(primary: number, secondary: number) {
        super(primary);
        this.secondary = secondary;
    }
}
"""
		self.maxDiff = 2048
		module = TSCore.createModuleFromWpp(source, 'superInCon.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))

	def testOverride(self):
		source = """
class First
	method virtual getValue: int
		param id: int
		return id * 2
class Second
	extends First
	method override getValue: int
		param id: int
		return super(id) + 1
"""
		expected = """
class First {
    getValue(id: number): number {
        return id * 2;
    }
}
class Second extends First {
    getValue(id: number): number {
        return super.getValue(id) + 1;
    }
}
"""
		self.maxDiff = 2048
		module = TSCore.createModuleFromWpp(source, 'superInOver.wpp')
		ctx = OutContextMemoryStream()
		module.exportContext(ctx, style)
		self.assertEqual(str(ctx), module.strPack(expected))
