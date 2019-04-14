if __name__=='__main__':
	import sys, os.path
	sys.path.append(os.path.abspath('../'))

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
				newTaxon.location = context.createLocation()
				newTaxon.readHead(context)
				postTaxon = stack[-1].addTaxon(newTaxon)
				stack.append(postTaxon)
		else:
			context.throwError('Invalid offset')

if __name__=='__main__':
	from Wpp.Context import Context
	from Wpp.WppModule import WppModule
	curDir = os.path.split(__file__)[0]
	ctx = Context.createFromFile(os.path.join(curDir, 'tests', 'files', 'simpleAB.wpp'))
	module = WppModule('simpleAB')
	readWpp(ctx, module)