from core.TaxonTypedef import TaxonTypedef
from TS.TsTaxon import TsTaxon

class TsTypedef(TaxonTypedef, TsTaxon):
	def __init__(self, name = None):
		super().__init__(name = name)
		self._hidden = False
		self._externName = ''

	def onUpdate(self):
		res = super().onUpdate()
		if self.owner.isClass() and not self._hidden:
			self._hidden = True
			if self.getReplaceMode() == 'extern':
				self._externName = self.altName or self.owner.getName(self)+self.name
				superOwner = self.owner.owner
				taxTypedef = self.creator('Typedef')(name = self._externName)
				taxTypedef.attrs = self.attrs.copy()
				taxTypedef.addItem(self.getTypeTaxon().cloneRoot(self.core))
				superOwner.addItem(taxTypedef, nextItem = self.owner)
				res = True
		return res

	def getReplaceMode(self):
		for mode in ['replace', 'extern']:
			if mode in self.attrs:
				return mode
		return self.getTypeTaxon().defaultReplaceMode()

	def exportUsage(self):
		if self._hidden:
			if self.getReplaceMode() == 'replace':
				return self.getTypeTaxon().exportString()
			if self.getReplaceMode() == 'extern':
				return self._externName
		return None

	def export(self, outContext):
		if self._hidden:
			return
		self.exportComment(outContext)
		s = 'type '+self.getName(self)+' = ' + self.getTypeTaxon().exportString() + ';'
		access = self.getAccessLevel()
		if self.owner.type == 'Module':
			access = 'export' if access == 'public' else ''
		if access:
			s = access + ' ' + s
		outContext.writeln(s)