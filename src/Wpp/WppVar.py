from core.TaxonVar import TaxonCommonVar, TaxonVar, TaxonField, TaxonReadonly, TaxonParam
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
		words = nameAndAttrs.split()
		self.init(words, typeDescr, valueDescr, context)

	def init(self, words, typeDescr, valueDescr, context):
		# parse main part with name and attrs
		if len(words) < 2:
			context.throwError('Expected name of ' + self.keyWord)
		self.name = words[-1]
		self.attrs |= set(words[1:-1])
		# parse type
		if typeDescr:
			self.addItem(WppType.create(typeDescr, context))
		else:
			self.items.append(None)
		if valueDescr:
			self.addItem(WppExpression.create(valueDescr, context))

	def export(self, outContext):
		chunks = [self.keyWord] + self.filteredAttrs() + [self.name]
		s = ' '.join(chunks) + ': ' + self.getLocalType().exportString()
		v = self.getValueTaxon()
		if v:
			s += ' = ' + v.exportString()
		outContext.writeln(s)
		outContext.level += 1
		self.exportComment(outContext)
		outContext.level -= 1

	defaultAccessLevel = ''
	def onUpdate(self):
		if self.defaultAccessLevel and not self.getAccessLevel():
			self.attrs.add(self.defaultAccessLevel)	# Если не указан квалификатор доступа, значит установить указанный по-умолчаеию
	def filteredAttrs(self):
		res = list(self.attrs)
		if self.defaultAccessLevel in self.attrs:
			res.remove(self.defaultAccessLevel)
		return res

class WppVar(TaxonVar, WppCommonVar):
	keyWord = 'var'

class WppField(TaxonField, WppCommonVar):
	keyWord = 'field'
	defaultAccessLevel = 'private'

class WppReadonly(TaxonReadonly, WppCommonVar):
	keyWord = 'readonly'
	defaultAccessLevel = 'public'

class WppParam(TaxonParam, WppCommonVar):
	keyWord = 'param'

	def readHead(self, context):
		""" Возможен вариант с init, который используется для создания конструкции this.id = id """
		pairs = context.currentLine.split('=', 1)
		words = pairs[0].split()
		if len(words) != 3 or words[1] != 'init':
			return super().readHead(context)
		self.init(words, None, pairs[1] if len(pairs) == 2 else None, context)

	def onUpdate(self):
		if 'init' in self.attrs and not self.getLocalType():
			self.setAutoInit()
		return super().onUpdate()

	def setAutoInit(self):
		# Специфичная конструкция - автоматическая инициализация типа this.id = id. Тип определяется из параметра
		myClass = self.findOwner('Class', True)
		field = myClass.dictionary.get(self.name)
		if not field:
			self.throwError('Not found field for auto init: "'+self.name+'"')
		srcType = field.getLocalType()
		dstType = srcType.clone(self.core)
		goodItems = self.items[1:]
		self.items = []
		self.addItem(dstType)
		self.items += goodItems
		self.setRef('field', field)

	def export(self, outContext):
		if 'init' not in self.attrs:
			super().export(outContext)
		else:
			s = 'param init ' + self.getName(self)
			expr = self.getValueTaxon()
			if expr:
				s += ' = ' + expr.exportString()
			outContext.writeln(s)
