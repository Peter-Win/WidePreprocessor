from core.ErrorTaxon import ErrorTaxon

class Context:
	""" Контекст для чтения универсального кода из файла
	"""
	__slots__ = ('fileName', 'lines', 'currentLine', 'nextIndex', 'taxonStack', 'lastLevel')

	@staticmethod
	def createFromFile(fileName):
		return Context(fileName)

	@staticmethod
	def createFromMemory(lines, name = None):
		if isinstance(lines, str):
			lines = lines.split('\n')
		return Context(name, lines)

	def __init__(self, fileName, lines = None):
		self.fileName = fileName
		if not lines:
			f = open(fileName)
			self.lines = f.readlines()
			f.close()
		else:
			self.lines = lines
		self.currentLine = ''
		self.nextIndex = 0	# номер строки в lines для чтения следующей строки в currentLine

	def createLocation(self):
		return (self.fileName, self.nextIndex, self.currentLine)

	def readLine(self):
		"Считать очередную строку. Обратный слеш приклеивает следующую строку. Пустые строки игнорируются"
		self.currentLine = ''
		while self.nextIndex < len(self.lines):
			ln = self.lines[self.nextIndex].rstrip()
			self.nextIndex += 1
			if len(ln) == 0:
				continue
			if ln.endswith('\\'):
				self.currentLine += ln[:-1]
			else:
				self.currentLine += ln
				break
		return self.currentLine

	def isFinish(self):
		return self.nextIndex >= len(self.lines) and not self.currentLine

	def getFirstWord(self):
		"Первое слово текущей строки"
		return self.currentLine.split()[0]

	def getCurrentLevel(self):
		"Уровень вложенности текущей строки"
		i = 0
		while (i < len(self.currentLine) and self.currentLine[i] == '\t'):
			i += 1
		return i

	def throwError(self, message):
		"Генерировать ошибку чтения"
		raise ErrorTaxon(message, self.createLocation())

if __name__ == '__main__':
	import os.path
	ctx = Context(os.path.abspath('../../examples/Point.wpp'))
	print('fileName: ', ctx.fileName)
	print('lines count: ', len(ctx.lines))

	for i in range(3):
		currentLine = ctx.readLine()
		print('currentLine:', currentLine)
		print('firstWord:', ctx.getFirstWord())
		print('level:', ctx.getCurrentLevel())

	try:
		ctx.throwError('Test')
	except Exception as e:
		print(str(e))
