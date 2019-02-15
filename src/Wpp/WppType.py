from core.TaxonType import TaxonType, TaxonTypeName, TaxonTypePath, TaxonTypeArray, TaxonTypeMap

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
			if word == 'Map':
				pair = splitComma(chunks[i+1:])
				if len(pair) < 2:
					context.throwError('Expected comma between key and value types')
				if len(pair) > 2:
					context.throwError('Too many commas in Map declaration')
				keyType = WppType.create(pair[0], context)
				valueType = WppType.create(pair[1], context)
				return WppTypeMap.create(keyType, valueType, attrs)
			if i == N - 1:
				# Type with reference by name
				if '.' in word:
					return WppTypePath(word, attrs)
				return WppTypeName(word, attrs)
			attrs.add(word)

def splitComma(chunks):
	groups = [[]]
	part = 0
	for word in chunks:
		if word[-1] != ',':
			groups[part].append(word)
		else:
			if word != ',':
				groups[part].append(word[0:-1])
			part += 1
			groups.append([])
	return groups


class WppTypeName(TaxonTypeName):
	def __init__(self, typeName=None, attrs=None):
		super().__init__()
		self._typeName = typeName
		if attrs:
			self.attrs = attrs

	def isOk(self):
		return 'type' in self.refs

	def onUpdate(self):
		class TaskWppTypeName:
			def check(self):
				return True
			def exec(self):
				taxon = self.taxon
				if not taxon._typeName:
					return
				if taxon._typeName.startswith('@'):
					# Если это шаблонный тип
					pass
				else:
					# Найти объявление типа
					decl = taxon.findUp(taxon._typeName, taxon, taxon)
					if not decl:
						taxon.throwError('Not found type "%s"' % (taxon._typeName))
					taxon.setRef('type', decl)
		self.addTask(TaskWppTypeName(), 'type')

	def exportString(self):
		chunks = self.getExportAttrs() + [self.getTypeTaxon().name]
		return ' '.join(chunks)

class WppTypePath(TaxonTypePath):
	def __init__(self, path='', attrs=None):
		super().__init__(path)
		if attrs:
			self.attrs |= attrs
	def exportString(self):
		chunks = self.getExportAttrs() + [self.path]
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

class WppTypeMap(TaxonTypeMap):
	@staticmethod
	def create(keyType, valueType, attrs):
		map = WppTypeMap()
		map.addItem(keyType)
		map.addItem(valueType)
		map.attrs |= attrs
		return map
	def exportString(self):
		chunks = list(self.attrs) + ['Map']
		s = ' '.join(chunks)
		s += ' ' + self.getKeyType().exportString()
		s += ', ' + self.getValueType().exportString()
		return s
