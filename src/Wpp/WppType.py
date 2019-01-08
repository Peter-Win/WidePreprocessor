from core.TaxonType import TaxonType, TaxonTypeName, TaxonTypeArray

class WppType(TaxonType):
	@staticmethod
	def create(description, context):
		"Создать тип из строкового описания"
		if not description:
			context.throwError("Can't create type from empty definition")
		chunks = description.split() if isinstance(description, str) else description
		N = len(chunks)
		attrs = set()
		for i, word in enumerate(chunks):
			if word == 'Array':
				return WppTypeArray(WppType.create(chunks[i+1:], context), attrs)
			if i == N - 1:
				# Type with reference by name
				return WppTypeName(word, attrs)
			attrs.add(word)

class WppTypeName(TaxonTypeName):
	def __init__(self, typeName=None, attrs=None):
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

class WppTypeArray(TaxonTypeArray):
	def __init__(self, itemType=None, attrs=None):
		super().__init__()
		if attrs:
			self.attrs = attrs
		if itemType:
			self.addItem(itemType)

	def exportString(self):
		chunks = list(self.attrs) + ['Array']
		return ' '.join(chunks) + ' ' + self.getItemType().exportString()
