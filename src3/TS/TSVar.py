from core.TaxonVar import TaxonVar, TaxonParam, TaxonField
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
	def __init__(self):
		super().__init__()
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
