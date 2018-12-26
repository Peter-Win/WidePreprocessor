from out.OutContextMemory import OutContextMemory

class OutContextMemoryStream(OutContextMemory):
	""" Всё подряд пишется в память """
	def createFolder(self, name):
		return self

	def createFile(self, name):
		return self