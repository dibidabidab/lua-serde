
from os import path, makedirs
from sys import argv
from glob import glob
from pathlib import Path

from load import readMultiAST
from template import renderStructs

if len(argv) != 4:
    print("Usage: ")
    print("lua-json-serde <outputdir> <inputdir> <includeheader>")
    exit(0)

outputDir = argv[1]
configs = glob(argv[2] + "/**/*.yaml", recursive=True)
includeHeader = argv[3]

if not path.exists(outputDir):
    makedirs(outputDir)

astList = readMultiAST(configs, includeHeader)
generatedFiles = []

def writeRender(render, filename):
    filePath = path.join(outputDir, filename)

    if Path(filePath).exists() and Path(filePath).read_text() == render:
        print("Skipping {}, unchanged".format(filename))
        return
    print("Writing  {}".format(filename))

    file = open(filePath, 'w')
    file.write(render)
    file.close()


for ast in astList:
    hpprender, cpprender = renderStructs(ast)

    writeRender(hpprender, ast['filename'] + '.hpp')
    writeRender(cpprender, ast['filename'] + '.cpp')
