from out.lexems import Lex

def exportLexemsPrior(taxon, lexems, rules):
	isBrackets = taxon.isNeedBrackets()
	if isBrackets: 
		lexems.append(Lex.bracketBegin)
	taxon.exportLexems(lexems, rules)
	if isBrackets:
		lexems.append(Lex.bracketEnd)
