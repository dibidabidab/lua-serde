#! /bin/python

import sys
import os

from load import readGlobAST
from template import renderStructs

if len(sys.argv) != 3:
    print("Usage: ")
    print("lua-cpp-serde <configs> <outputdir>")
    exit(0)

configGlob = sys.argv[1]
outputDir = sys.argv[2]

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

astList = readGlobAST(configGlob)
generatedFiles = []

for ast in astList:
    render = renderStructs(ast)

    basename, ext = os.path.splitext(ast['filename'])
    filename = basename + '.hpp'
    generatedFiles.append(filename)

    file = open(os.path.join(outputDir, filename), 'w')
    file.write(render)
    file.close()

file = open(os.path.join(outputDir, 'include_all.hpp'), 'w')
file.writelines(['#include "' + filename + '"' for filename in generatedFiles])
file.close()
