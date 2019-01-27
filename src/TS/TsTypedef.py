from core.TaxonTypedef import TaxonTypedef
from TS.TsTaxon import TsTaxon

class TsTypedef(TaxonTypedef, TsTaxon):
	def export(self, outContext):
		self.exportComment(outContext)
		s = 'type '+self.getName(self)+' = ' + self.getTypeTaxon().exportString() + ';'
		access = self.getAccessLevel()
		if self.owner.type == 'Module':
			access = 'export' if access == 'public' else ''
		if access:
			s = access + ' ' + s
		outContext.writeln(s)