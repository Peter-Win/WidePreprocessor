from core.TaxonVar import TaxonVar, TaxonParam
from Python.PyTaxon import PyTaxon
from Python.PyExpression import PyConst
from out.lexems import Lex

class PyVar(TaxonVar, PyTaxon):
	def onInit(self):
		if not self.getValueTaxon():
			# Если нет значения, то назначить дефолтное для типа значение, т.к. в питоне тип определяется значением
			val = self.getTypeTaxon().createDefaultValue()
			self.addItem(val)

	def exportLexems(self, level, lexems, rules):
		""" Экспорт объявления переменной, как отдельной строки """
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
