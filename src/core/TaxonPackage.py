from TaxonDictionary import TaxonDictionary

class TaxonPackage(TaxonDictionary):
	""" Пакет. Контейнер для группы модулей и других пакетов.
	Для Wpp-сообщества (и большинства других) это директория.
	Но для JS может осуществляться объединение пакетов и модулей в один файл.
	"""
	type = 'Package'

	def export(self, outContext):
		newContext = outContext.createFolder(self.name)
		for item in self.items:
			item.export(newContext)

	def findUp(self, name, fromWho, source):
		""" Поиск внутри пакета предполагает, что надо искать во вложенных пакетах и модулях
		"""
		if self.name == name:
			return self
		results = []
		for i in self.items:
			if i != fromWho:
				# Имя модуля не участвует в поиске. Т.к. часто имя класса совпадает с именем модуля. И нужно находить класс, а не модуль
				if i.name == name and i.type != 'Module':
					return i
				results += i.findDown(name)
		if len(results) == 1:
			return results[0]
		# Вполне возможно, что в разных пакетах будут таксоны с одинаковыми именами
		# В этом случае нужно сгенерировать ошибку. Т.к. для точного указания нужно имя пакета
		if len(results) > 1:
			msg = 'Multiply declaration of "'+name+'" in ['
			msg += ', '.join([res.getPath() for res in results]) + ']'
			source.throwError(msg)
		if self.owner:
			return self.owner.findUp(name, self, source)

	def findDown(self, name):
		""" Поиск вниз для пакета предполагает обход всех подчиненных
		Потому что это подчиненные пакеты или модули
		"""
		results = []
		if self.name == name:	# Пакеты участвуют в поиске по имени, в отличие от модулей
			results.append(self)
		for i in self.items:
			results += i.findDown(name)
		return results
