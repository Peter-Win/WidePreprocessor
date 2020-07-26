import re

def isUpperCamelCase(name):
	return not not re.fullmatch(r'^[A-Z][A-Za-z0-9]*$', name)

def isLowerCamelCase(name):
	return not not re.fullmatch(r'^[a-z][A-Za-z0-9]*$', name)

def checkLowerCamelCase(name, txType):
	if not isLowerCamelCase(name):
		return 'lowerCamelCase is required for %s name "%s"' % (txType, name)

def checkUpperCamelCase(name, txType):
	if not isUpperCamelCase(name):
		return 'UpperCamelCase is required for %s name "%s"' % (txType, name)
