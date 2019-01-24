class Rect:
	""" Rectangle object """
	__slots__ = ('A', 'B')
	def __init__(self):
		self.A = None
		self.B = None
	def init(self, xa, ya, xb, yb):
		""" Init rect by number coordinates """
		self.A.init(xa, ya)
		self.B.init(xb, yb)

