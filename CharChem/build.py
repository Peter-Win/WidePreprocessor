import os
import sys
sys.path.append(os.path.realpath('../src'))

from Wpp.WppCore import WppCore
from Python.PyCore import PyCore
from out.OutContextFolder import OutContextFolder
from out.deleteTree import deleteTree

rootPath = os.path.dirname(os.path.abspath(__file__))

wppPath = os.path.join(rootPath, 'wpp')
print('Build CharChem. Reading from '+wppPath)
core = WppCore()
srcRoot = core.createRootPackage('CharChem', wppPath)

outPath = os.path.join(rootPath, 'Python')
print('Export to '+outPath)
dstRoot = srcRoot.cloneRoot(PyCore())
deleteTree(outPath)
os.mkdir(outPath)
outContext = OutContextFolder(outPath)
dstRoot.export(outContext)

print('Success')