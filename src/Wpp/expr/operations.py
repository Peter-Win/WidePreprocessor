binOps = {
	'=': 15,
	'+=': 15,
	'-=': 15,
	'*=': 15,
	'/=': 15,
	'||': 14,
	'&&': 13,
	'|': 12,
	'^': 11,
	'&': 10,
	'>': 8,
	'<': 8,
	'>=': 8,
	'<=': 8,
	'==': 8,
	'!=': 8,
	'<<': 7,
	'>>': 7,
	'+': 6,
	'-': 6,
	'*': 5,
	'/': 5,
	'%': 5,
	'.': 2,
}
unOps = {
	'-': 3,
	'!': 3,
	'~': 3,
}
fnArgsPrior = 2
squareBracketPrior = 2
ternaryPrior = 15

specChars = ''
specWordsList = sorted(['(', ')', '[', ']', '?', ':', ','] + list(binOps.keys()) + list(unOps), reverse=True)
specCharsSet = set()
for word in specWordsList:
	for c in word: specCharsSet.add(c)
for c in specCharsSet:
	specChars += c
specWords = set(specWordsList)
