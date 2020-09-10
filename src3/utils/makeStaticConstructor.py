""" TODO: в дальнейшем можно оптимизировать. Чтобы сразу вызывать конструктор праметрами, которые полностью инициализируют объект.
В Wpp запрещено объявлять дефолтные параметры в перегруженных функциях, но в питоне нет перегрузок. Поэтому возможен более оптимальный код:
class simple Point                    class Point:
  field x: double                       __slots__ = ('x', 'y')
  field y: double                       def __init__(self, x = 0, y = 0):
  constructor overload                    self.x = x
    x = 0                                 self.y = y
    y = 0                               @staticmethod
  constructor overload                  def copyPoint(src):
    altName initPoint                     return Point(src.x, src.y)
    autoinit x
    autoinit y
  constructor overload                  Здесь удалось совместить два конструктора в одном за счет использования дефолтных параметров
    altName copyPoint
    param src: const ref Point
    x = src.x
    y = src.y
"""
from core.TaxonAltName import TaxonAltName

def makeStaticConstructor(conImpl):
	"""
	conImpl - Имплементация перегруженного конструктора. type = constructor
	"""
	# Check altName
	name = TaxonAltName.getAltName(conImpl, 'overloaded constructor')
	conImpl.attrs.add('useAltName')
	conImpl.attrs.add('static')
	cls = conImpl.findOwnerByType('class');
	# Set result type
	t = conImpl.addItem(conImpl.creator('@typeExprName')(cls.getName()))
	t.setType(cls)

	body = conImpl.getBody()
	instName = '_inst'
	# создание экземпляра класса при помощи конструктора с пустыми параметрами.
	inst = body.addItem(conImpl.creator('var')(instName), 0)
	inst.attrs.add('const')
	t = inst.addItem(conImpl.creator('@typeExprName')())
	t.setType(cls)
	txNew = inst.addItem(conImpl.creator('new')())
	caller = txNew.addItem(conImpl.creator('named')(cls.getName()))
	caller.setTarget(cls)
	# Замена всех this на обращение к _inst
	def changeThis(taxon):
		if taxon.type == 'this':
			taxon.replaceTaxon(conImpl.creator('named')(instName)).setTarget(inst)
	body.walk(changeThis)
	# return of created instance
	ret = body.addItem(conImpl.creator('return')())
	retExpr = ret.addItem(conImpl.creator('named')(instName))
	retExpr.setTarget(inst)

	inst.initAll()
