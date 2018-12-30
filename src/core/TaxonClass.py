from TaxonDictionary import TaxonDictionary

class TaxonClass (TaxonDictionary):
	type = 'Class'

	def getParent(self):
		return self.refs.get('ext')

	def getMembers(self):
		""" Члены класса в виде списка """
		return self.items

	def findUp(self, name, fromWho, source):
		""" Переопределенная фунция класса Taxon
		Позволяет искать среди членов класса, но не спускаясь в них
		"""
		if self.name == name:
			return self
		for i in self.items:
			if i != fromWho:
				if i.name == name:
					return i
		if self.owner:
			return self.owner.findUp(name, self, source)
