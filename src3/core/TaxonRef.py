from Taxon import Taxon

class TaxonRef(Taxon):
	"""
	Ссылки нужны для указания на те таксоны, которые не принадлежат владельцу ссылки.
	Например, у переменной есть тип, но переменная лишь ссылается на него. А сам таксон типа чаще всего принадлежит ядру.
	Ссылка имеет два механизма: создание и клонирование.
	Создание происходит при загрузке из wpp. При этом таксон обычно предварительно ищется по имени.
	При клонировании происходит поиск через путь
	"""
	type = '@reference'

	@staticmethod
	def fromTaxon(target):
		ref = TaxonRef()
		ref.setTarget(target)
		return ref

	def __init__(self):
		super().__init__()
		self.target = None
		self.path = None

	def setTarget(self, taxon):
		self.target = taxon

	def getTarget(self):
		return self.target

	def copyFieldsFrom(self, src):
		# При копировании целевой объект остает ся пуст, а путь берется из исходного таксона
		super().copyFieldsFrom(src)
		self.target = None
		self.path = src.target.getPathExt()

	def onInitRef(self):
		# Этот код выполняется после копирования всех элементов, но до вызова initAll
		if not self.path:
			self.throwError('Path is not init')
		# При загрузке Wpp уходит много времени на поиск объектов по довольно сложным правилам.
		# Но здесь можно сразу получить ссылку на целевой объект при помощи пути
		# Путь должен работать одинаково в исходном и новом сообществе.
		self.target = self.core.findByPathExt(self.path)
