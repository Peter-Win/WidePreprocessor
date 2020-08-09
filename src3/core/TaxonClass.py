"""
Классы в WPP максимально близки к тем, которые используются в Java.
Предполагается автоматичкская сборка мусора. Поэтому деструктор не поддерживается.
Желательно придерживаться правила, принятого в Java - один public класс на модуль. И имя модуля совпадает с именем файлаю
Родительский класс может быть только один (или ни одного).
Но есть возможность реализации нескольких интерфейсов.
Три уровня доступа к членам класса: public, protected, private. Для полей по-умолчанию private, для методов - public
Поддерживаются статические методы и поля.
Поля можно инициализировать присваиванием в объявлении. (есть в Java, TS. Нет в C++, Python)
Класс может быть абстрвктным.
Разрешена перегрузка методов, в том числе и конструкторов.
Однако, переопределяемые функции должны быть отмечены атрибутами virtual|abstract и override, что больше похоже на C++
Класс может быть объявлен в модуле.
Основное отличие от С++, что там нет сборки мусора. Поэтому для C++ нужно делать реализацию с подсчетом ссылок.
  Но есть атрибут simple для обозначения простых классов, экземпляры которых не используют heap. Например, Point.
Отличие от Java в возможности использовать дефолтные параметры в методах.
Отличия от Python, EcmaScript6+, TypeScript и др скриптов:
 - Не предполагается возможность поиска элементов класса по имени в рантайме. Типа hasattr в питоне или inst['fieldName'] в ES6.
 - Не поддерживается утиная типизация. То есть одинаковый состав полей не позволяет приводить один тип к другому. Важны только родственные отношения.

Для доступа к своим членам класса из методов не требуется использование this.
"""
from TaxonDict import TaxonDict

class TaxonClass(TaxonDict):
	type = 'class'

	def isClass(self):
		return True

	def getExtends(self):
		for taxon in self.items:
			if 'extends' in taxon.attrs:
				return taxon
		return None

	def setExtends(self, classTaxon):
		ref = TaxonRef.fromTaxon(classTaxon)
		ref.attrs.add('extends')
		self.addItem(ref)

	def getImplements(self):
		pass

	def getMembers(self):
		# Все члены класса обязательно поименованы
		return [taxon for taxon in self.items if taxon.name]

	@staticmethod
	def getAccessLevelFor(taxon):
		for level in ['public', 'private', 'protected']:
			if level in taxon.attrs:
				return level
