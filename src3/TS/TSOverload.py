"""
Большинство скриптовых языков не поддерживают перегрузку функций.
Потому что там выполняется поиск по имени в словаре во время выполения.
Но TypeScript имеет продвинутый механизм.
В нем можно задекларировать несколько сигнатур.
Но реализация все равно одна, где нужно анализировать тип параметров.

Дефолтная реализация требует наличия altName и определяет перегруженные функции как имеющие оазные имена.
"""

from core.TaxonOverload import TaxonOverload
from core.TaxonAltName import TaxonAltName

class TSOverload(TaxonOverload):
	def onInit(self):
		for taxon in self.items:
			altName = TaxonAltName.getAltName(taxon)
			if not altName:
				# Если перегружаются конструкторы, то altName не требуется для конструктора без параметров
				if taxon.type == 'constructor' and len(taxon.getParamsList()) == 0:
					continue
				taxon.throwError('altName is required for overloaded %s' % (taxon.getDebugStr()))
			taxon.attrs.add('useAltName')

	def exportLexems(self, lexems, style):
		for taxon in self.items:
			taxon.exportLexems(lexems, style)