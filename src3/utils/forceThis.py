def forceThis(taxonNamed):
	"""
	Во многих языках необходимо явно указывать this при обращении к членам класса.
	К ним относятся: Python, TypeScript, JavaScript, PHP
	Но в WPP это не является обязательным, как в Java или C++
	Поэтому при трансформации из WPP в языки из первого списка для Named-выражений, которые неявно обращаются к членам класса
	нужно вызывать эту функцию

	Параметр taxonNamed - таксон типа TaxonNamed, независимо от типа целевого таксона, на который ссылается имя.
	Проверка типа выполняется внутри функции. Если тип не подходящий, то ничего не выполняется и возврашается False
	Если taxonNamed указывает на член класса, то производится замена конструкции fieldName на this.fieldName

	"""
	target = taxonNamed.getTarget()
	if target.type not in {'field', 'method'}:
		return False
	# TODO: Пока не учитывается ситуция, где target явдяется статическим членом. Т.к. желательно в таких случаях явно указывать имя класса.
	dot = taxonNamed.creator('dot')(taxonNamed.targetName)
	this = taxonNamed.creator('this')()
	this.setTarget(target.owner)
	dot.addItem(this)
	taxonNamed.replaceTaxon(dot)
	return True