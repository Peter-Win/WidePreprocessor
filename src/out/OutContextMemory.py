
class OutContextMemory:
	def __init__(self):
		self.lines = []
		self.level = 0

	def writeln(self, string):
		self.lines.append('\t' * self.level + string)
	def close(self):
		pass
	def __str__(self):
		return '\n'.join(self.lines)