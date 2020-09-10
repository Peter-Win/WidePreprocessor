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

Простые классы используются для математических объектов. Для них можно определять операторы.
Важное отличие: копирование простых объектов происходит по значению, а не по ссылке. Как в C++
Поэтому параметры с простыми объектами желательно объявлять с атрибутами const ref
"""
from TaxonDict import TaxonDict
from core.QuasiType import QuasiType

class TaxonClass(TaxonDict):
	type = 'class'

	def isClass(self):
		return True
	def isType(self):
		return True

	def getDebugStr(self):
		return '%s %s' % (self.type, self.getName())
		
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

	def getFields(self):
		return [taxon for taxon in self.getMembers() if taxon.type == 'field']

	@staticmethod
	def getAccessLevelFor(taxon):
		for level in ['public', 'private', 'protected']:
			if level in taxon.attrs:
				return level

	def buildQuasiType(self):
		return QuasiType(self)

	def matchQuasiType(self, left, right):
		rightTaxon = right.taxon
		if right.taxon == left.taxon:
			return 'exact', None
		return None, None

	def findConstructor(self):
		"""
		Возможно три разных результата:
		None, если конструктора нет
		type == 'constructor', если у класса один конструктор
		type == 'overload', если несколько конструкторов
		"""
		for taxon in self.items:
			if taxon.type == 'constructor':
				return taxon
			if taxon.type == 'overload' and 'constructor' in taxon.attrs:
				return taxon
		return None

	def isAllFieldsInit(self):
		""" True, если все поля имеют значения """
		for field in self.getFields():
			if not field.getValueTaxon():
				return False
		return True

	def isNeedAutoConstructor(self):
		""" True, если требуется неявный конструктор 
		Например, в TypeScript или Java достаточно указать начальные значения полей класса и можно не писать конструктор.
		А в Python, Ruby или C++ нужно сгенерировать конструктор без парметров с явной инициализацией полей.
		"""
		if len(self.getFields()) == 0:
			return False
		con = self.findConstructor()
		if not con or con.type != 'overload':
			return False
		for taxon in con.items:
			if len(taxon.getParamsList()) == 0:
				return False
		return True
