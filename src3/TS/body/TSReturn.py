from core.body.TaxonReturn import TaxonReturn
from out.lexems import Lex
from core.body.TaxonBody import TaxonBody
from core.TaxonFunc import TaxonFunc

class TSReturn(TaxonReturn):
	def exportLexems(self, lexems, rules):
		expr = self.getResult()
		if 'shortForm' in self.owner.attrs:
			# В cлучае короткой формы нужно экспортировать только выражение
			expr.exportLexems(lexems, rules)
			return

		lexems.append(Lex.keyword('return'))
		if expr:
			lexems.append(Lex.space)
			expr.exportLexems(lexems, rules)
		lexems.append(Lex.instrDiv)

	def onInit(self):
		# Нужно различать короткий синтаксис без оператора return
		# Для этого в body должен быть всего один элемент
		if self.getResult() and isinstance(self.owner, TaxonBody) and self.owner.owner.type == 'func' and len(self.owner.items) == 1:
			# В этом случае body получает атрибут shortForm, который учитывается при экспорте
			self.owner.attrs.add('shortForm')
