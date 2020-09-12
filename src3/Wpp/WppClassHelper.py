from core.TaxonFunc import TaxonFunc
from core.TaxonClass import TaxonClass

def checkMemberAccess(source, target):
	"""
	Проверка возможности доступа к члену класса
	source представлен таксоном типа WppNamed
	target - член класса
	"""
	# Нужно найти метод, в котором находится source
	sourceMethod = source.owner
	while not (sourceMethod.owner.isClass() and isinstance(sourceMethod, TaxonFunc)):
		if sourceMethod.isModule():
			sourceMethod = None
			break
		sourceMethod = sourceMethod.owner

	# Если target не является статическим, а source принадлежит статическому члену, это ошибка
	if not target.isStatic() and sourceMethod and sourceMethod.isStatic():
		source.throwError('Non-static %s "%s" cannot be referenced from the static "%s"' % (target.type, target.getName(), sourceMethod.getName()))

	TaxonClass.checkAccess(source, target)
