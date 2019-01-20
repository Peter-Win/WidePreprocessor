class Point:
	""" 2D Point (or vector) object """
	__slots__ = ('x', 'y')
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def init(self, newX, newY):
		""" Reusing a point instance with new values.
		 Returns this point object with new x, y values. """
		self.x = newX
		self.y = newY
		return self
	def fromPoint(self, pt):
		""" Copying a point from another object """
		self.x = pt.x
		self.y = pt.y
	def clone(self):
		""" Point cloning """
		return Point(self.x, self.y)
	@staticmethod
	def is0(a):
		return a == 0
	def __eq__(self, pt):
		return (is0(self.x - pt.x)) && (is0(self.y - pt.y))

