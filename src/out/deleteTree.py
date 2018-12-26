import os
def deleteTree(path):
	if not os.path.isdir(path):
		return
	for name in os.listdir(path):
		fullName = os.path.join(path, name)
		if os.path.isdir(fullName):
			deleteTree(fullName)
		else:
			os.remove(fullName)
	os.rmdir(path)
