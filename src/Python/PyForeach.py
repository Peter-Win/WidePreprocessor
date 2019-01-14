from core.TaxonForeach import TaxonForeach
from Python.PyTaxon import PyTaxon

class PyForeach(TaxonForeach, PyTaxon):
	def export(self, outContext):
		s = 'for '
		index = self.getIndex()
		value = self.getValue()
		if index:
			s += index.getName(self)
			s += ', '
		s += value.getName(self)
		s += ' in '
		collection = self.getCollection()
		collectionType = collection.getDeclaration().getLocalType()
		s += collectionType.exportCollection(collection, index)
		s += ':'
		outContext.writeln(s)
		self.getBody().export(outContext)