from core.TaxonVar import TaxonVar, TaxonParam, TaxonField
from Python.PyTaxon import PyTaxon
from Python.PyExpression import PyConst
from out.lexems import Lex

def forceValue(taxon):
	if not taxon.getValueTaxon():
		# Если нет значения, то назначить дефолтное для типа значение, т.к. в питоне тип определяется значением
		val = taxon.getTypeTaxon().createDefaultValue()
		taxon.addItem(val)

class PyVar(TaxonVar, PyTaxon):
	def onInit(self):
		forceValue(self)

	def exportLexems(self, level, lexems, rules):
		""" Экспорт объявления переменной, как отдельной строки """
		self.exportExternalComment(level, lexems, rules)
		line = [Lex.varName(self.getName()), Lex.binop('=')]
		self.getValueTaxon().exportLexems(level, line, rules)
		self.exportLine(level, lexems, rules, line)

class PyParam(TaxonParam):
	def exportLexems(self, level, lexems, rules):
		lexems.append(Lex.varName(self.getName()))
		val = self.getValueTaxon()
		if val:
			lexems.append(Lex.binop('='))
			val.exportLexems(level, lexems, rules)

class PyField(TaxonField, PyTaxon):
	def onInit(self):
		forceValue(self)

	def exportLexems(self, level, lexems, style):
		self.exportExternalComment(level, lexems, style)
		line = [Lex.keyword('self'), Lex.dot, Lex.varName(self.getName()), Lex.binop('=')]
		self.getValueTaxon().exportLexems(0, line, style)
		self.exportLine(level, lexems, style, line)
