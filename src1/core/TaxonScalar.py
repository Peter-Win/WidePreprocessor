from Taxon import Taxon
from core.QuasiType import QuasiType

constMatchesInt = {'int': 'constExact'}
constMatchesFloat = {'float': 'constExact', 'int': 'constUpcast'}

class TaxonScalar(Taxon):
	type = 'TypeScalar'
	propsList = [
		('bool', {'bool': 'constExact'}, {'bool': 'exact'}),
		('int8', constMatchesInt, {'int8': 'exact'}),
		('short', constMatchesInt, {'short': 'exact', 'int8': 'upcast'}),
		('int', constMatchesInt, {'int': 'exact', 'short': 'upcast', 'int8': 'upcast'}),
		('long', constMatchesInt, {'long': 'exact', 'int': 'upcast', 'short': 'upcast', 'int8': 'upcast'}),
		('float', constMatchesFloat, {'float': 'exact'}),
		('double', constMatchesFloat, {'double': 'exact', 'float': 'upcast'}),
	]
	@staticmethod
	def createByName(typeName):
		for props in TaxonScalar.propsList:
			if props[0] == typeName:
				return TaxonScalar(props)
		raise 'Invalid scalar type ' + typeName

	def __init__(self, props):
		name, matchConst, matchVar = props
		super().__init__(name)
		self.matchConst = matchConst
		self.matchVar = matchVar

	def isType(self):
		return True
	def isReadyFull(self):
		return True
	def getFinalType(self, attrs):
		return self, attrs

	def buildQuasiType(self):
		return QuasiType(self)

	def matchQuasiType(self, left, right): #TODO: Проверять unsigned и диаазон констант
		if right.isType('Const'):
			result = self.matchConst.get(right.taxon.constType)
			if result and right.taxon.value[0]=='-' and ('unsigned' in left.attrs):
				return None, 'Conversion from "%s" to "%s"' % (right.taxon.value, left.exportString())
			return result, None
		if right.isType(TaxonScalar.type):
			result = self.matchVar.get(right.taxon.name)
			return result, None
		return None, None

	def getDebugStr(self):
		return '::' + self.name
	def exportString(self):
		return self.typePrefix() + self.name