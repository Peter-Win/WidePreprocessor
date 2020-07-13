import os
from out.OutContextFile import OutContextFile

class OutContextFolder:
	""" Контекст вывода, который соответствует папке.
	Объект контекста создаётся для существующей папки.
	"""
	def __init__(self, path):
		self.path = path

	def createFolder(self, name):
		newPath = os.path.join(self.path, name)
		os.mkdir(newPath)
		return OutContextFolder(newPath)

	def createFile(self, name):
		return OutContextFile(os.path.join(self.path, name))
