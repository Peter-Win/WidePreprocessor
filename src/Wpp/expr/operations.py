binOps = {
	'=': 5,
	'+=': 5,
	'-=': 5,
	'*=': 5,
	'/=': 5,
	'||': 6,
	'&&': 7,
	'|': 8,
	'^': 9,
	'&': 10,
	'>': 12,
	'<': 12,
	'>=': 12,
	'<=': 12,
	'==': 12,
	'!=': 12,
	'<<': 13,
	'>>': 13,
	'+': 14,
	'-': 14,
	'*': 15,
	'/': 15,
	'%': 15,
	'.': 18,
}
unOps = {
	'-': 17,
	'!': 17,
	'~': 17,
}
fnArgsPrior = 18
squareBracketPrior = 18
ternaryPrior = 5

specChars = ''
specWordsList = sorted(['(', ')', '[', ']', '?', ':', ','] + list(binOps.keys()) + list(unOps), reverse=True)
specCharsSet = set()
for word in specWordsList:
	for c in word: specCharsSet.add(c)
for c in specCharsSet:
	specChars += c
specWords = set(specWordsList)
