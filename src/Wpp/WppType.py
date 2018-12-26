from core.TaxonType import TaxonType, TaxonTypeName

class WppType(TaxonType):
	@staticmethod
	def create(description, context):
		"Создать тип из строкового описания"
		chunks = description.split() if isinstance(description, str) else description
		N = len(chunks)
		attrs = set()
		for i, word in enumerate(chunks):
			if i == N - 1:
				# Type with reference by name
				return WppTypeName(word, attrs)
			attrs.add(word)

class WppTypeName(TaxonTypeName):
	def __init__(self, typeName, attrs=None):
		super().__init__()
		self._typeName = typeName
		if attrs:
			self.attrs = attrs

	def onUpdate(self):
		if self._typeName:
			# Найти объявление типа
			decl = self.findUp(self._typeName, self, self)
			if not decl:
				self.throwError('Not found type "'+self._typeName+'"')
			self.refs['type'] = decl
			self._typeName = None

	def exportString(self):
		chunks = list(self.attrs) + [self.getTypeTaxon().name]
		return ' '.join(chunks)