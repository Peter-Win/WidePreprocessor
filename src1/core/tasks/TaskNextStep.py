class TaskNextStep:
	""" Задача, которая выполняется на следующем шаге """
	def __init__(self):
		self.bReady = False
	def check(self):
		prevValue = self.bReady
		self.bReady = True
		return prevValue
	def exec(self):
		pass
