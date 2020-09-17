import glob
import yaml


def readGlobStructs(configGlob):
    paths = glob.glob(configGlob)
    structs = [readStructs(path) for path in paths]
    return [struct for struct1d in structs for struct in struct1d]


def readStructs(path):
    file = open(path)
    structs = yaml.load(file, Loader=yaml.FullLoader)
    print(structs)
    return structs
