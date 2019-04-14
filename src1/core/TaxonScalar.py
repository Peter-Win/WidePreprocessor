from Taxon import Taxon

intMatches = {'int': 'constExact'}
floatMatches = {'fixed': 'constExact', 'float': 'constExact', 'int': 'constNear'}

class TaxonScalar(Taxon):
	type = 'TypeScalar'
	propsList = [
		('bool', {'bool': 'constExact'}),
		('int8', {'int8': 'constExact'}),
		('short', {'int8': 'constNear', 'short': 'constExact'}),
		('int', intMatches),
		('long', intMatches),
		('float', floatMatches),
		('double', floatMatches),
	]

	def __init__(self, props):
		name, matchConst = props
		super().__init__(name)
		self.matchConst = matchConst

	def isType(self):
		return True
	def isReadyFull(self):
		return True
	def getFinalType(self, attrs):
		return self, attrs
	def validate(self, valueTaxon, attrs):
		if valueTaxon.type == 'Const':
			constType = valueTaxon.constType
			# Возможно ли присваивание переменной данному типу
			if constType not in self.matchConst:
				return "NotFound"
			# Проверка беззнаковых типов
			if 'unsigned' in attrs:
				value = valueTaxon.getRealValue()
				if value < 0:
					return 'Conversion from "%s" to "unsigned %s"' % (valueTaxon.value, self.name)
			return ''
		# if valueTaxon.type == 'IdExpr':
		if hasattr(valueTaxon, 'typeRef'):
			typeRef, newAttrs = valueTaxon.typeRef.getFinalType(attrs)
			if typeRef.type == 'TypeScalar' and typeRef.name in self.matchConst:
				return ''
		return "NotFound"

