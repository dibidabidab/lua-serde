#! /bin/python

import sys

import load

if len(sys.argv) != 3:
    print("Usage: ")
    print("lua-cpp-serde <configs> <outputdir>")
    exit(0)

configGlob = sys.argv[1]
outputDir = sys.argv[2]

structures = load.readGlobStructs(configGlob)
