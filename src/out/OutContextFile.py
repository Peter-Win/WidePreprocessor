class OutContextFile:
	def __init__(self, fileName):
		self.fileName = fileName
		self.file = open(fileName, 'w')
		self.level = 0

	def writeln(self, string):
		self.file.write('\t' * self.level + string + '\n')

	def close(self):
		self.file.close()
