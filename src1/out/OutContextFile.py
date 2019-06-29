from out.OutContextBase import OutContextBase
class OutContextFile(OutContextBase):
	def __init__(self, fileName):
		super().__init__()
		self.fileName = fileName
		self.file = open(fileName, 'w')

	def writeln(self, string):
		self.file.write('\t' * self.level + string + '\n')

	def tab(self):
		self.file.write('\t' * self.level)
	def out(self, string):
		self.file.write(string)
	def eol(self):
		self.file.write('\n')

	def close(self):
		self.file.close()
