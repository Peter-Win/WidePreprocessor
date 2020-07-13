"""
var [public] <varName> : <typeExpression> [ = <initialValue]
param [ref|ptr] <paramName: <typeExpression> [ = <defaultValue>]
field [public|private|protected|static] <fieldName> : <typeExpression> [ = <initialValue>]
"""
from core.TaxonVar import TaxonVar, TaxonField, TaxonParam
from Wpp.WppTypeExpr import WppTypeExpr
from Wpp.WppExpression import WppExpression
from Wpp.WppTaxon import WppTaxon
from core.QuasiType import QuasiType

class WppCommonVar(WppTaxon):
	def commonVarInit(self, context, name, attrs, typeExpr, initialValue = None):
		self.name = name
		self.attrs |= attrs
		txTypeExpr = WppTypeExpr.parse(typeExpr, context)
		self.addItem(txTypeExpr)
		if initialValue != None:
			txValue = WppExpression.parse(initialValue, context)
			self.addItem(txValue)


	def readHead(self, context):
		if len(self.items) != 0:
			context.throwError('Secondary readHead call')
		self._location = context.createLocation()

		errorMsg, name, attrs, typeDescr, valueDescr = self.parseHead(context.currentLine)
		if errorMsg:
			context.throwError(errorMsg)
		else:
			self.commonVarInit(context, name, attrs, typeDescr, valueDescr)

	@staticmethod
	def parseHead(line):
		""" parse string description """
		pair = line.split(':', 1)
		if len(pair) != 2:
			return ('Expected ":" for type declaration', None, None, None, None)
		nameAndAttrs = pair[0]
		typeAndValue = pair[1]
		pair2 = typeAndValue.split('=', 1)
		typeDescr = pair2[0].strip()
		valueDescr = pair2[1].strip() if len(pair2) == 2 else None 
		words = nameAndAttrs.split()
		# parse main part with name and attrs
		if len(words) < 2:
			return ('Expected name of ' + words[0], None, None, None, None)
		name = words[-1]
		attrs = set(words[1:-1])

		return (None, name, attrs, typeDescr, valueDescr)

	def onCommonInit(self):
		txType = self.getTypeTaxon()
		if not txType:
			self.throwError('Type expression is not initialized')

		# Если есть const, значит должно быть выражение, TODO: возможно не для параметра
		txVal = self.getValueTaxon()
		if 'const' in self.attrs and not txVal:
			self.throwError('Expected value of const')

		# Здесь надо ждать готовности, чтобы проверить типы
		if txVal:
			class TaskWait:
				def check(self):
					return txType.buildQuasiType() and txVal.buildQuasiType()
				def exec(self):
					self.taxon.checkType()
			self.addTask(TaskWait())

	def checkType(self):
		left = self.getTypeTaxon()
		right = self.getValueTaxon()
		result, errMsg = QuasiType.matchTaxons(left, right)
		if errMsg:
			self.throwError(errMsg)


class WppVar(TaxonVar, WppCommonVar):
	def export(self, outContext):
		result = ['var'] + self.getExportAttrs() + [self.name + ':'] + [self.getTypeTaxon().exportString()]
		val = self.getValueTaxon()
		if val:
			result += ['=', val.exportString()]
		outContext.writeln(' '.join(result))

	def onInit(self):
		self.onCommonInit()

class WppField(TaxonField):
	pass

class WppParam(TaxonParam):
	pass