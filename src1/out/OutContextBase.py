class OutContextBase:
	def __init__(self):
		self.level = 0
	def __enter__(self):
		self.push()
	def __exit__(self, a, b, c):
		self.pop()
	def push(self):
		self.level += 1
	def pop(self):
		self.level -= 1