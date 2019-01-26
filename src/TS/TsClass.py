from core.TaxonClass import TaxonClass
from TS.TsTaxon import TsTaxon

class TsClass(TaxonClass, TsTaxon):
	def export(self, outContext):
		self.exportComment(outContext)
		s = 'class ' + self.getName(self)
		if self.getAccessLevel() == 'public':
			s = 'export ' + s
		parent = self.getParent()
		if parent:
			s += ' extends ' + parent.getName(self)
		s += ' {'
		outContext.writeln(s)
		outContext.level += 1
		for item in self.items:
			item.export(outContext)
		outContext.level -= 1
		outContext.writeln('}')
