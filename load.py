import glob
import yaml
import os


def readGlobAST(configGlob):
    paths = glob.glob(configGlob)
    return [readAST(path) for path in paths]


def readAST(path):
    file = open(path)
    structs = yaml.load(file, Loader=yaml.FullLoader)
    return prepareAST(structs, os.path.basename(path))


def popOr(dict, key, default):
    if key in dict:
        return dict.pop(key)
    return default


def prepareAST(structs, filename):
    config = popOr(structs, 'config', {})
    for key in structs:
        structs[key] = prepareStruct(structs[key])

    return {
        'config': config,
        'structs': structs,
        'filename': filename,
    }


def prepareStruct(struct):
    cpp_only = popOr(struct, '_cpp_only', {})
    methods = popOr(struct, '_methods', [])

    return {
        'expose': prepareVars(struct),
        'cpp_only': prepareVars(cpp_only),
        'methods': methods,
    }


def prepareVars(dict):
    prepared = []
    for key, value in dict.items():
        if type(value) is list:
            typ, default = value
            prepared.append({
                'name': key,
                'typ': typ,
                'default': default,
            })
        else:
            prepared.append({
                'name': key,
                'typ': value,
            })
    return prepared
