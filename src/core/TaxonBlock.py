from Taxon import Taxon

class TaxonBlock(Taxon):
	type = 'Block'
	def findUp(self, name, fromWho, source):
		# Поиск в блоке предполагает, что нужно искать объявления локальных переменных, но обявленных выше fromWho
		for cmd in self.items:
			if cmd == fromWho:
				break
			if cmd.type == 'Var' and cmd.name == name:
				return cmd
		return self.owner.findUp(name, fromWho, source)

	def getQuasiType(self):
		# Вызов функции из тела. Н.р. someFunc(...)
		# Означает, что результат игнорируется
		return None
	def isQuasiReady(self):
		return True