from core.TaxonLocalType import TaxonLocalType, TaxonTypeName, TaxonTypeArray, TaxonTypeMap
from core.Ref import Ref

class WppLocalType(TaxonLocalType):
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
				return WppTypeArray(WppLocalType.create(chunks[i+1:], context), attrs)
			if word == 'Map':
				pair = splitComma(chunks[i+1:])
				if len(pair) < 2:
					context.throwError('Expected comma between key and value types')
				if len(pair) > 2:
					context.throwError('Too many commas in Map declaration')
				keyType = WppLocalType.create(pair[0], context)
				valueType = WppLocalType.create(pair[1], context)
				return WppTypeMap(keyType, valueType, attrs)
			if i == N - 1:
				# Type with reference by name
				# if '.' in word:
				# 	return WppTypePath(word, attrs)
				return WppTypeName.create(word, attrs)
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
	@staticmethod
	def create(name, attrs):
		inst = WppTypeName()
		inst.typeRef = Ref(name)
		inst.attrs = attrs
		return inst
	def exportString(self):
		chunks = self.getExportAttrs() + [self.typeRef.name]
		return ' '.join(chunks)

	def onUpdate(self):
		result = super().onUpdate()
		typeTarget = self.typeRef.target
		if not typeTarget.isType():
			self.throwError('Invalid type: ' + typeTarget.type)
		return result

class WppTypeArray(TaxonTypeArray):
	def __init__(self, itemType=None, attrs=None):
		super().__init__()
		if attrs:
			self.attrs = attrs
		if itemType:
			self.addItem(itemType)

	def exportString(self):
		chunks = self.getExportAttrs() + ['Array']
		return ' '.join(chunks) + ' ' + self.getItemType().exportString()

class WppTypeMap(TaxonTypeMap):
	def __init__(self, keyType, valueType, attrs):
		super().__init__()
		self.addItems([keyType, valueType])
		self.attrs = arres
	def exportString(self):
		chunks = self.getExportAttrs() + ['Map']
		return '%s %s, %s' % (' '.join(chunks), self.getKeyType().exportString(), self.getValueType().exportString())
