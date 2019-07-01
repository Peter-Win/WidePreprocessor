from Taxon import Taxon

class TaxonBlock(Taxon):
	type = 'Block'
	def findUp(self, fromWho, params):
		# Поиск в блоке предполагает, что нужно искать объявления локальных переменных, но обявленных выше fromWho
		for cmd in self.items:
			if cmd == fromWho:
				break
			if (cmd.type == 'Var' or cmd.type == 'Typedef') and cmd.isMatch(params):
				return cmd
		return self.owner.findUp(fromWho, params)

	def getQuasiType(self):
		# Вызов функции из тела. Н.р. someFunc(...)
		# Означает, что результат игнорируется
		return None

	def getDebugStr(self):
		return 'BLOCK'

	def isReady(self):
		return True

	def isReadyFull(self):
		return True
