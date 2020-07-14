from core.TaxonVar import TaxonVar
from TS.TSTaxon import TSTaxon
from out.lexems import Lex

class TSVar(TaxonVar, TSTaxon):
	def exportLexems(self, lexems, rules):
		self.exportComment(lexems, rules)
		if self.owner.isModule() and 'public' in self.attrs:
			lexems += [Lex.keyword('export'), Lex.space]
		lexems += [Lex.keyword('const' if 'const' in self.attrs else 'let'),
			Lex.space, Lex.varName(self.getName()),
		]
		# Возможна ситуация, когда тип не указывается при объявлении. Если он следует из выражения
		txType = self.getTypeTaxon()
		if txType:
			lexems.append(Lex.colon)
			txType.exportLexems(lexems, rules)

		txValue = self.getValueTaxon()
		if txValue:
			lexems.append(Lex.binop('='))
			txValue.exportLexems(lexems, rules)

		lexems.append(Lex.instrDiv)
