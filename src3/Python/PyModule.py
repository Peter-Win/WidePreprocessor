from core.TaxonModule import TaxonModule
from Python.style import style
from out.formatter import formatLexems

class PyModule(TaxonModule):
	__slots__ = ()
	def exportLexems(self, lexems, rules):
		# сначала нужно вывести импорты
		# далее экспорт всех подчиненных таксонов
		for taxon in self.items:
			taxon.exportLexems(0, lexems, rules)

	def exportText(self, rules):
		""" Экспорт в виде списка строк """
		lexems = []
		self.exportLexems(lexems, rules)
		rows= []
		formatLexems(rows, lexems, 0, 0, rules)
		return rows

	def exportContext(self, context, style):
		for row in self.exportText(style):
			context.writeln(row)
