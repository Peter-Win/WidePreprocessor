from TaxonDictionary import TaxonDictionary

class TaxonPackage(TaxonDictionary):
	""" Пакет. Контейнер для группы модулей и других пакетов.
	Для Wpp-сообщества (и большинства других) это директория.
	Но для JS может осуществляться объединение пакетов и модулей в один файл.
	"""
	type = 'Package'

	def export(self, outContext):
		newContext = outContext.createFolder(self.name)
		self.onNewFolder(newContext)
		for item in self.items:
			item.export(newContext)

	def onNewFolder(self, outContext):
		pass

	def findUp(self, fromWho, params):
		""" Поиск внутри пакета предполагает, что надо искать во вложенных пакетах и модулях
		"""
		if self.isMatch(params):
			return self
		results = []
		for i in self.items:
			if i != fromWho:
				if i.isMatch(params):
					return i
				results += i.findDown(params)
		if len(results) == 1:
			return results[0]
		# Вполне возможно, что в разных пакетах будут таксоны с одинаковыми именами
		# В этом случае нужно сгенерировать ошибку. Т.к. для точного указания нужно имя пакета
		if len(results) > 1:
			msg = 'Multiply declaration of "%s" in [%s]' % (params['name'], ', '.join([res.getPath() for res in results]))
			params['source'].throwError(msg)
		if self.owner:
			return self.owner.findUp(self, params)

	def findDown(self, params):
		""" Поиск вниз для пакета предполагает обход всех подчиненных
		Потому что это подчиненные пакеты или модули
		"""
		return self._findDownRecursive(params)
