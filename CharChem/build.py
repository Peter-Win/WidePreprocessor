import os
import sys
sys.path.append(os.path.realpath('../src'))

from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from TS.TsCore import TsCore
from out.OutContextFolder import OutContextFolder
from out.deleteTree import deleteTree

rootPath = os.path.dirname(os.path.abspath(__file__))

def exportProject(srcRoot, dirName, core):
	outPath = os.path.join(rootPath, dirName)
	print('Export to ' + outPath)
	dstRoot = srcRoot.cloneRoot(core)
	deleteTree(outPath)
	os.mkdir(outPath)
	outContext = OutContextFolder(outPath)
	dstRoot.export(outContext)


wppPath = os.path.join(rootPath, 'wpp')
print('Build CharChem. Reading from '+wppPath)
core = WppCore()
srcRoot = core.createRootPackage('CharChem', wppPath)

# exportProject(srcRoot, 'Python', PyCore())
exportProject(srcRoot, 'TypeScript', TsCore())

print('Success')