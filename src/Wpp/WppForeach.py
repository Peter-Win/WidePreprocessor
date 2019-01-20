"""
Full syntax:
	for collection => var value => var index
		body
Short syntax:
	for collection => var value
		body
Possible case, but not recommended:
	var value: ItemType
	var index: IndexType
	for collection => value => index
"""
from core.TaxonForeach import TaxonForeach
from Wpp.WppTaxon import WppTaxon
from Wpp.expr.parseExpr import parseExpr
from Wpp.expr.scanLexems import scanLexems
from Wpp.WppBlock import WppBlock
from Wpp.WppVar import WppVar

class WppForeach(TaxonForeach, WppTaxon):
	def __init__(self):
		super().__init__()
		self.valueId = None
		self.indexId = None
		self.phase = 0

	def readHead(self, context):
		self.addItem(WppBlock())
		pair = context.currentLine.split(' ', 1)
		lexems = parseExpr(pair[1], context)
		node, pos = scanLexems(lexems, 0, {'=>'}, context)
		collection = node.makeTaxon()
		self.addItem(collection)

		# value
		pos += 1
		value, lexemType, constType = lexems[pos]
		if value == 'var' and lexemType == 'id':
			# Для значения создается новая переменная
			pos += 1
			value, lexemType, constType = lexems[pos]
			if lexemType != 'id':
				context.throwError('Expected variable name for value')
			self.attrs.add('localValue')
			varValue = WppVar()
			varValue.name = value
			self.addItem(varValue)
			self.setRef('value', varValue)
		else:
			if lexemType != 'id':
				context.throwError('Expected variable name for value')
			self.valueId = value

		# index (optional)
		pos += 1
		value, lexemType, constType = lexems[pos]
		if lexemType == 'cmd' and value == '=>':
			pos += 1
			value, lexemType, constType = lexems[pos]
			if value == 'var' and lexemType == 'id':
				pos += 1
				value, lexemType, constType = lexems[pos]
				if lexemType != 'id':
					context.throwError('Expected variable name for index')
				self.attrs.add('localIndex')
				varIndex = WppVar()
				varIndex.name = value
				self.addItem(varIndex)
				self.setRef('index', varIndex)
			else:
				if lexemType != 'id':
					context.throwError('Expected variable name for index')
				self.indexId = value

	def readBody(self, context):
		return self.getBody().readBody(context)

	def addTaxon(self, taxon):
		return self.getBody().addTaxon(taxon)

	def findUp(self, name, fromWho, source):
		if self.isValueLocal() and self.getValue().name == name:
			return self.getValue()
		if self.isIndexLocal() and self.getIndex().name == name:
			return self.getIndex()
		return super().findUp(name, fromWho, source)

	def onUpdate(self):
		self.phase += 1
		if self.phase == 1:
			if self.valueId:
				varValue = self.owner.findUpEx(self.valueId)
				self.setRef('value', varValue)
			if self.indexId:
				varIndex = self.owner.findUpEx(self.indexId)
				self.setRef('index', varIndex)
			return True
		if len(self.items) == 2:
			collection = self.getCollection()
			collectionDecl = collection.getDeclaration()
			collectionLocalType = collectionDecl.getLocalType()
			itemType = collectionLocalType.getItemType()
			#TODO: ...

	def export(self, outContext):
		s = 'foreach '
		s += self.getCollection().exportString()
		s += ' => '
		if self.isValueLocal():
			s += 'var '
		s += self.getValue().getName(self)
		i = self.getIndex()
		if i:
			s += ' => '
			if self.isIndexLocal():
				s += 'var '
			s += i.getName(self)
		outContext.writeln(s)

		outContext.level += 1
		self.getBody().export(outContext)
		outContext.level -= 1