from Taxon import Taxon
from out.OutContextBase import OutContextBase

class OutContextMemory(OutContextBase):
	def __init__(self):
		super().__init__()
		self.lines = []
		self.curLine = ''

	def writeln(self, string):
		self.lines.append('\t' * self.level + string)

	# Функции низкоуровневого вывода
	def tab(self):
		self.curLine = '\t' * self.level
	def out(self, string):
		self.curLine += string
	def eol(self):
		self.lines.append(self.curLine)
		self.curLine = ''

	def close(self):
		pass
	def __str__(self):
		return Taxon.strPack('\n'.join(self.lines))