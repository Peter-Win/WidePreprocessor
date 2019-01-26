import unittest
from Wpp.WppCore import WppCore
from out.OutContextMemoryStream import OutContextMemoryStream

class TestBool(unittest.TestCase):
	def testBool(self):
		source = """
func public boolName: String
	param value: bool
	value ? "Yes" : "No"

func public trueName: String
	boolName(true)

func public falseName: String
	boolName(false)
		"""
		module = WppCore.createMemModule(source, 'bool.fake')
		trueNameOver = module.dictionary['trueName']
		trueName = trueNameOver.items[0]
		cmd = trueName.getBody().items[0]
		self.assertEqual(cmd.type, 'Return')
		expr = cmd.getExpression()
		self.assertEqual(expr.type, 'Call')
		params = expr.getArguments()
		p1 = params[0]
		self.assertEqual(p1.type, 'True')

		outContext = OutContextMemoryStream()
		module.export(outContext)
		self.assertEqual(str(outContext), module.strPack(source))