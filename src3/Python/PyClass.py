from core.TaxonClass import TaxonClass
from Python.PyTaxon import PyTaxon
from out.lexems import Lex


class PyClass(TaxonClass, PyTaxon):
	"""
	Конструкция питоновского класса несколько отличается от WPP. Поэтому потребуется приличное количество преобразований.
	- Не статические поля класса объявляются внутри конструктора.
	- Используется __slots__ для фиксации полей
	- Запрещена перегрузка методов
	"""

	def exportLexems(self, level, lexems, style):
		line = [Lex.keyword('class'), Lex.space, Lex.className(self.getName())]
		parent = self.getParent()
		if parent:
			line += [Lex.bracketBegin, Lex.className(parent.getName()), Lex.bracketEnd]
		# Интерфейсы включать нет смысла, т.к в питоне утиная типизация, а наличие реализуемых методов проверяется в WPP
		line.append(Lex.colon)
		self.exportLine(level, lexems, style, line)

		bodyLevel = level + 1
		self.exportInternalComment(bodyLevel, lexems, style)

		# Разделить члены класса по категориям
		staticFields = []
		fields = []
		methods = []

		if len(self.getMembers()) == 0:
			self.exportLine(bodyLevel, lexems, style, [Lex.keyword('pass')])
		
		for member in self.getMembers():
			if member.type == 'field':
				if member.isStatic():
					staticFields.append(member)
				else:
					fields.append(member)
			elif member.type in ('method', 'operator', 'overload'):
				methods.append(member)
			# TODO: потом появятся конструктор, операторы и тп

		# Обозначить список нестатических полей через __slots__
		if len(fields) > 0:
			line = [Lex.keyword('__slots__'), Lex.binop('='), Lex.bracketBegin]
			for f in fields:
				line.append(Lex.stringRaw(f.getName(), style))
				line.append(Lex.itemDiv)
			line[-1] = Lex.itemDivLast
			line.append(Lex.bracketEnd)
			self.exportLine(bodyLevel, lexems, style, line)

		# Список статическиз полей (точнее, в питоне это переменныхе класса. но работают так же как статические)
		for field in staticFields:
			line = [Lex.varName(field.getName()), Lex.binop('=')]
			field.getValueTaxon().exportLexems(0, line, style)
			self.exportLine(bodyLevel, lexems, style, line)

		# Поля надо определить в конструкторе
		con = self.findConstructor()
		if con == None:
			self.exportZeroConstructor(bodyLevel, lexems, style, fields)
		else:
			if self.isNeedAutoConstructor():
				self.exportZeroConstructor(bodyLevel, lexems, style, fields)
			con.exportLexems(bodyLevel, lexems, style)

		# Методы
		for method in methods:
			method.exportLexems(bodyLevel, lexems, style)

	def exportZeroConstructor(self, level, lexems, style, fields):
		"""
		Для исходного класса конструктор не определен. Значит его полностью формируем под определение полей
		"""
		if len(fields) == 0:
			return
		line = [Lex.keyword('def'), Lex.space, Lex.keyword('__init__'), Lex.paramsBegin, Lex.keyword('self'), Lex.paramsEnd, Lex.colon]
		self.exportLine(level, lexems, style, line)
		for field in fields:
			field.exportLexems(level + 1, lexems, style)

