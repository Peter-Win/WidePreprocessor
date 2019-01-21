class Point:
	""" 2D Point (or vector) object """
	__slots__ = ('x', 'y')
	def __init__(self, x = 0.0, y = 0.0):
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
		return abs(a) < 0.001
	def __eq__(self, pt):
		return is0(self.x - pt.x) and is0(self.y - pt.y)
	def iaddn(self, x, y):
		""" Point operator += (x, y) """
		self.x += x
		self.y += y
		return self
	def __iadd__(self, pt):
		self.x += pt.x
		self.y += pt.y
		return self
	def addn(self, x, y):
		""" Add external numbers. Point operator + (x, y) """
		return Point(self.x + x, self.y + y)
	def __add__(self, pt):
		""" Add external point. Point operator + (Point) """
		return Point(self.x + pt.x, self.y + pt.y)
	def isubn(self, x, y):
		""" Subtraction internal numbers. Point operator -= (x, y) """
		self.x -= x
		self.y -= y
		return self
	def __isub__(self, pt):
		""" subtraction internal (Point) """
		self.x -= pt.x
		self.y -= pt.y
		return self
	def subn(self, x, y):
		""" Point operator - (x, y) """
		return Point(self.x - x, self.y - y)
	def __sub__(self, pt):
		""" Point operator - (Point) """
		return Point(self.x - pt.x, self.y - pt.y)
	def __neg__(self):
		return Point(-self.x, -self.y)
	def iminn(self, x1, y1):
		""" min internal numbers """
		self.x = min(self.x, x1)
		self.y = min(self.y, y1)
		return self
	def imin(self, pt):
		""" min internal (Point) """
		return iminn(pt.x, pt.y)
	def imaxn(self, x1, y1):
		""" max internal numbers """
		self.x = max(self.x, x1)
		self.y = max(self.y, y1)
		return self
	def imax(self, pt):
		""" max internal (Point) """
		return imaxn(pt.x, pt.y)
	def ineg(self):
		""" negative internal: pt = -pt """
		self.x = -self.x
		self.y = -self.y
		return self
	def __imul__(self, k):
		""" internal multiply by coefficient """
		self.x *= k
		self.y *= k
		return self
	def __mul__(self, k):
		return Point(self.x * k, self.y * k)
	def __rmul__(self, k):
		return Point(k * self.x, k * self.y)
	def lengthSqr(self):
		""" square of length """
		return self.x ** 2 + self.y ** 2
	def length(self):
		""" Length """
		return sqrt(lengthSqr())
	def distSqrn(self, x1, y1):
		""" Square of distance to point, defined by numbers """
		return (self.x - x1) ** 2 + (self.y - y1) ** 2
	def distSqr(self, pt):
		""" Square of distance to point """
		return self.distSqrn(pt.x, pt.y)
	def dist(self, pt):
		""" Distance to point """
		return sqrt(self.distSqr(pt))

