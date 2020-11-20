from core.TaxonOverload import TaxonOverload
from out.lexems import Lex
from Python.PyTaxon import PyTaxon

class PyOverload(TaxonOverload):

	def onInit(self):
		from core.TaxonAltName import TaxonAltName
		for taxon in self.items:
			altName = TaxonAltName.getAltName(taxon)
			if not altName:
				# Если перегружаются конструкторы, то altName не требуется для конструктора без параметров
				if taxon.type == 'constructor' and len(taxon.getParamsList()) == 0:
					continue
				# У операторов возможно наличие разных имен за счет использования атрибута right
				if taxon.type == 'operator' and self.getCountOfName(taxon.getName()) == 1:
					continue
				taxon.throwError('altName is required for overloaded %s' % (taxon.getDebugStr()))
			taxon.attrs.add('useAltName')

	def exportLexems(self, level, lexems, style):
		for taxon in self.items:
			taxon.exportLexems(level, lexems, style)