def readWpp(context, owner, baseLevel = 0):
	stack = [owner]
	while not context.isFinish():
		line = context.readLine()
		if not line.strip():
			continue
		currentLevel = context.getCurrentLevel() + baseLevel
		while currentLevel + 1 < len(stack):
			last = stack.pop()
		if currentLevel + 1 == len(stack):
			newTaxon = stack[-1].readBody(context)
			if newTaxon:
				if not newTaxon._location:
					newTaxon._location = context.createLocation()
				newTaxon.readHead(context)
				postTaxon = stack[-1].addTaxon(newTaxon)
				stack.append(postTaxon)
		else:
			context.throwError('Invalid offset')
