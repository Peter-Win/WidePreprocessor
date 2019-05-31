import unittest
from Taxon import Taxon
from core.Signature import Signature
from core.TaxonScalar import TaxonScalar
from core.TaxonFunc import TaxonFunc
from core.TaxonVar import TaxonParam, TaxonVar
from core.TaxonLocalType import TaxonTypeName
from core.Ref import Ref
from core.QuasiType import QuasiType

typeInt = TaxonScalar.createByName('int')
typeFloat = TaxonScalar.createByName('float')
typeShort = TaxonScalar.createByName('short')
typeLong = TaxonScalar.createByName('long')
typeDict = {t.name:t for t in [typeInt, typeFloat, typeShort, typeLong]}

class MyVar(Taxon):
	def __init__(self, name, typeRef):
		super().__init__(name)
		self.typeRef = typeRef
	def buildQuasiType(self):
		return QuasiType.combine(self, self.typeRef)
	def exportString(self):
		return '%s:%s' % (self.name, self.typeRef.name)
	def getDebugStr(self):
		return 'MyVar(%s)' % (self.exportString())

def createParam(descr):
	pair = descr.split(':')
	typeName = pair[1]
	param = TaxonParam(pair[0])
	paramType = TaxonTypeName()
	paramType.typeRef = Ref(typeName, typeDict[typeName])
	param.addItem(paramType)
	return param

def createFunc(name, params):
	func = TaxonFunc(name)
	for tax in [Taxon('body')] + [createParam(p) for p in params]:
		func.addItem(tax)
	return func

class TestSignature(unittest.TestCase):
	def testStr(self):
		sign = Signature()
		sign.params = [MyVar('i', typeInt), MyVar('x', typeFloat)]
		self.assertEqual(str(sign), 'i:int; x:float')
	def testMatch(self):
		sign = Signature()
		sign.params = [MyVar('i', typeInt), MyVar('x', typeFloat)]
		fn1 = createFunc('fn1', ['i:int', 'x:float'])
		args1 = fn1.getParams()
		self.assertEqual(len(args1), 2)
		self.assertEqual(args1[0].type, 'Param')
		self.assertEqual(QuasiType.matchTaxons(sign.params[0], args1[0]), ('exact', None))	# int exact int
		self.assertEqual(QuasiType.matchTaxons(sign.params[1], args1[0])[0], None) # int variable can't upcast to float
		self.assertEqual(QuasiType.matchTaxons(sign.params[0], args1[1])[0], None) # float can't upcast to int
		self.assertEqual(QuasiType.matchTaxons(sign.params[1], args1[1]), ('exact', None)) # float exact float
		self.assertEqual(sign.match(fn1), 6) # exact = 3, upcast = 1
		fn2 = createFunc('fn2', ['a:long', 'b:float'])
		self.assertEqual(QuasiType.matchTaxons(fn2.getParams()[0], sign.params[0]), ('upcast', None)) # long = int -> upcast
		self.assertEqual(QuasiType.matchTaxons(fn2.getParams()[1], sign.params[1]), ('exact', None)) # float = float -> exact
		self.assertEqual(sign.match(fn2), 4) # exact=3 + upcast(1) = 4
