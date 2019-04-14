class ErrorTaxon(RuntimeError):
	def __str__(self):
		message = self.args[0]
		location = self.args[1] if len(self.args) > 1 else None
		text = '*Error* ' + message
		if location:
			fileName, lineNumber, string = location
			if fileName:
				text += ' in file ' + fileName + ', line ' + str(lineNumber)
			if string:
				text += ': ' + string
		return text
