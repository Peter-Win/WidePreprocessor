import unittest
from Wpp.WppCore import WppCore
from Wpp.Context import Context
from out.OutContextMemory import OutContextMemory
from out.OutContextMemoryStream import OutContextMemoryStream

class TestWppFunc(unittest.TestCase):
	def testFuncSimple(self):
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory('func simple1', 'simple1.fake'))
		self.assertIn('simple1', module.dictionary)
		over = module.dictionary['simple1']
		self.assertEqual(over.type, 'Overloads')
		self.assertEqual(over.name, 'simple1')
		self.assertEqual(len(over.items), 1)
		self.assertIn('public', over.attrs) # Autoincluded by module
		func = over.items[0]
		self.assertEqual(func.type, 'Func')
		self.assertEqual(func.name, 'simple1')
		self.assertIsNone(func.getResultType())
		self.assertEqual(func.getParams(), [])

	def testFuncWithResult(self):
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory('func pure simple2: int', 'simple2.fake'))
		over = module.dictionary['simple2']
		func = over.items[0]
		self.assertEqual(func.name, 'simple2')
		self.assertIn('pure', func.attrs)
		taxonResult = func.getResultType()
		self.assertEqual(taxonResult.type, 'TypeName')
		
		outContext = OutContextMemory()
		func.export(outContext)
		self.assertEqual(str(outContext), 'func pure simple2: int')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), 'func pure simple2: int')

	def testFuncWithParams(self):
		source = """
func func03: double
	# with params
	param in x: double = 0
	param in y: double = -1
		"""
		core = WppCore()
		module = core.createRootModule(Context.createFromMemory(source, 'func03.fake'))
		over = module.dictionary['func03']
		func = over.items[0]
		params = func.getParams()
		self.assertEqual(len(params), 2)
		self.assertIn('x', func.dictionary)
		self.assertEqual(params[1].name, 'y')
		self.assertEqual(params[1].type, 'Param')

		outContext = OutContextMemory()
		params[0].export(outContext)
		self.assertEqual(str(outContext), 'param in x: double = 0')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())

	def testAltName(self):
		source = """
func func05
	altname hello
		"""
		module = WppCore.createMemModule(source, 'func05.fake')

		funcOver = module.dictionary['func05']
		self.assertEqual(funcOver.type, 'Overloads')
		func = funcOver.items[0]
		self.assertEqual(func.type, 'Func')
		self.assertEqual(func.name, 'func05')
		self.assertEqual(func.altName, 'hello')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), source.strip())
		
