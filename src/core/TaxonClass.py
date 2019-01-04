from TaxonDictionary import TaxonDictionary

class TaxonClass (TaxonDictionary):
	type = 'Class'
	canBeStatic = True

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

	def findConstructor(self):
		from core.TaxonFunc import TaxonConstructor
		return self.dictionary.get(TaxonConstructor.key)

	def createEmptyConstructor(self):
		taxonMap = self.core.taxonMap
		con = taxonMap['Constructor']()
		over = taxonMap['Overloads']()
		over.name = con.name
		self.addNamedItem(over)
		over.addItem(con)
		con.addItem(taxonMap['Block']())
		# Переместить конструктор на первое место...
		for pos, item in enumerate(self.items):
			if item.type == over.type: break
		if item != over:
			self.items.pop()
			self.items.insert(pos, over)
		return con

