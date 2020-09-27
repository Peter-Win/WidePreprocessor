from core.TaxonVar import TaxonVar, TaxonParam, TaxonField, TaxonAutoinit
from TS.TSTaxon import TSTaxon
from out.lexems import Lex
from core.TaxonClass import TaxonClass

def optimiseType(taxon):
	# Если тип переменной следует из выражения, его можно не указывать
	val = taxon.getValueTaxon()
	if val:
		t = taxon.getTypeTaxon()
		taxon.removeItem(t)
		taxon.hiddenType = t

def exportVar(var, lexems, rules):
	if var.type == 'field':
		lexems.append(Lex.fieldName(var.getName()))
	else:
		lexems.append(Lex.varName(var.getName()))
	# Возможна ситуация, когда тип не указывается при объявлении. Если он следует из выражения
	txType = var.getTypeTaxon()
	if txType:
		lexems.append(Lex.colon)
		txType.exportLexems(lexems, rules)

	txValue = var.getValueTaxon()
	if txValue:
		lexems.append(Lex.binop('='))
		txValue.exportLexems(lexems, rules)


class TSVar(TaxonVar, TSTaxon):
	def __init__(self, name = ''):
		super().__init__(name)
		self.hiddenType = None

	def onInit(self):
		optimiseType(self)

	def exportLexems(self, lexems, rules):
		self.exportComment(lexems, rules)
		if self.owner.isModule() and 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		lexems += [Lex.keyword('const' if 'const' in self.attrs else 'let'), Lex.space]
		exportVar(self, lexems, rules)
		lexems.append(Lex.instrDiv)

class TSField(TaxonField, TSTaxon):
	def onInit(self):
		optimiseType(self)

	def exportLexems(self, lexems, rules):
		self.exportComment(lexems, rules)
		# access level
		accessLevel = TaxonClass.getAccessLevelFor(self)
		if accessLevel:
			lexems += [Lex.keyword(accessLevel), Lex.space]
		# static
		if 'static' in self.attrs:
			lexems += [Lex.keyword('static'), Lex.space]
		exportVar(self, lexems, rules)
		lexems.append(Lex.instrDiv)

class TSParam(TaxonParam, TSTaxon):
	def onInit(self):
		optimiseType(self)

	def exportLexems(self, lexems, rules):
		exportVar(self, lexems, rules)

class TSAutoinit(TaxonAutoinit, TSTaxon):
	def onInit(self):
		self.createStdImplementation()

	def exportLexems(self, lexems, rules):
		lexems.append(Lex.varName(self.getName()))
		val = self.getValueTaxon()
		if val:
			lexems.append(Lex.binop('='))
			val.exportLexems(lexems, rules)
		else:
			lexems.append(Lex.colon)
			self.getTypeTaxon().exportLexems(lexems, rules)
