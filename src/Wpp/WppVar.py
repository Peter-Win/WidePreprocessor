from core.TaxonVar import TaxonCommonVar, TaxonVar, TaxonField, TaxonParam
from Wpp.WppTaxon import WppTaxon
from Wpp.WppType import WppType
from Wpp.WppExpression import WppExpression

class WppCommonVar(TaxonCommonVar, WppTaxon):
	def readHead(self, context):
		# parse string description
		pair = context.currentLine.split(':', 1)
		if len(pair) != 2:
			context.throwError('Expected ":" for type declaration')
		nameAndAttrs = pair[0]
		typeAndValue = pair[1]
		pair2 = typeAndValue.split('=', 1)
		typeDescr = pair2[0]
		valueDescr = pair2[1] if len(pair2) == 2 else None 
		# parse main part with name and attrs
		words = nameAndAttrs.split()
		if len(words) < 2:
			context.throwError('Expected name of ' + self.keyWord)
		self.name = words[-1]
		self.attrs |= set(words[1:-1])
		# parse type
		self.addItem(WppType.create(typeDescr, context))
		if valueDescr:
			self.addItem(WppExpression.create(valueDescr, context))

	def export(self, outContext):
		chunks = [self.keyWord] + list(self.attrs) + [self.name]
		s = ' '.join(chunks) + ': ' + self.getLocalType().exportString()
		v = self.getValueTaxon()
		if v:
			s += ' = ' + v.exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		outContext.level -= 1

class WppVar(TaxonVar, WppCommonVar):
	keyWord = 'var'

class WppField(TaxonField, WppCommonVar):
	keyWord = 'field'
	def onUpdate(self):
		if not self.getAccessLevel():
			self.attrs.add('private')	# Если не указан квалификатор доступа, значит это private

class WppParam(TaxonParam, WppCommonVar):
	keyWord = 'param'
