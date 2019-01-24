from core.TaxonType import TaxonTypeName, TaxonTypeArray, TaxonTypeMap, TaxonTypePath

class PyTypeName(TaxonTypeName):
	pass

class PyTypePath(TaxonTypePath):
	pass

class PyTypeArray(TaxonTypeArray):
	def exportCollection(self, user, bUseIndex):
		s = user.exportString()
		if bUseIndex:
			s = 'enumerate('+s+')'
		return s

class PyTypeMap(TaxonTypeMap):
	def exportCollection(self, user, bUseIndex):
		s = user.exportString()
		if bUseIndex:
			# Обычно словари используются с использованием ключа
			# Цикл foreach не может использоваться только с использованием ключа
			# Поэтому наиболее вероятный вариант - ключ, значение
			return s + '.items()'
		else:
			# Это менее вероятно, но необходимо для полноты
			return s + '.values()'