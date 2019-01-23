class TaxonImportBlock:
	""" Блок импортов.
	Не клонируется, т.к. в каждом языке свои правила импорта
	"""
	def __init__(self):
		self.dict = {}

	def addImport(self, importRecord):
		key = importRecord.getKey()
		if key in self.dict:
			self.dict[key].append(importRecord)
		else:
			self.dict[key] = importRecord

	def export(self, outContext):
		pass

	def isEmpty(self):
		return len(self.dict) == 0

class TaxonImport:
	def __init__(self, path):
		self.path = path
	def getKey(self):
		return self.path
	def append(self, importRecord):
		pass