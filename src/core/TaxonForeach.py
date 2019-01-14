from Taxon import Taxon

class TaxonForeach(Taxon):
	""" for index, value in collection {body}"""
	type = 'Foreach'
	def getBody(self):
		return self.items[0]
	def getCollection(self):
		return self.items[1]
	def getValue(self):
		return self.refs['value']
	def isValueLocal(self):
		return 'localValue' in self.attrs
	def getIndex(self):
		return self.refs.get('index')
	def isIndexLocal(self):
		return 'localIndex' in self.attrs